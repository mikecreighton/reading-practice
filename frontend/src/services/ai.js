const getBaseURL = () => {
  let baseURL = import.meta.env.VITE_API_URL ? import.meta.env.VITE_API_URL : ""

  // Strip out any trailing slashes from the base URL.
  baseURL = baseURL.replace(/\/$/, "")

  return baseURL
}

export const detectOpenAI = async () => {
  let baseURL = getBaseURL()
  return fetch(baseURL + "/openai_available", {
    method: "GET",
  })
    .then((response) => response.json())
    .then((data) => data.message)
}

export const generateStory = async (words, characterName, setting, humor, grade, abortSignal) => {
  let baseURL = getBaseURL()

  let payload = JSON.stringify({
    words: words,
    subject: characterName,
    setting: setting,
    humor: humor + "",
    grade: grade,
  })

  return fetch(baseURL + "/generate_story", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: payload,
    signal: abortSignal,
  })
    .then((response) => {
      if (!response.ok) {
        if (response.status === 429) {
          throw new Error("You've made too many requests. Please try again later.")
        }
        throw new Error("There was an error generating your story. Please try again.")
      }
      return response.json()
    })
    .then((data) => {
      if (!data.safe) {
        throw new Error(data.error)
      }
      return data.story
    })
    .catch((error) => {
      throw error
    })
}

export const generateIllustration = async (story, grade, abortSignal) => {
  let baseURL = getBaseURL()

  let payload = JSON.stringify({
    story: story,
    grade: grade,
    aspect_ratio: window.innerWidth > 768 ? "landscape" : "square",
  })

  return fetch(baseURL + "/generate_illustration", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: payload,
    signal: abortSignal,
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("There was an error generating your story. Please try again.")
      }
      return response.json()
    })
    .then((data) => {
      if (data.error) {
        throw new Error(data.error)
      }
      // data.image is a base64 encoded string but it doesn't have a data:image/jpeg;base64, prefix
      return "data:image/jpeg;base64," + data.image
    })
    .catch((error) => {
      throw error
    })
}
