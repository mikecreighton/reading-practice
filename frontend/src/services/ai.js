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

export const checkSafety = async (words, subject, setting, grade, abortSignal) => {
  let baseURL = getBaseURL()

  let payload = JSON.stringify({
    words: words,
    subject: subject,
    setting: setting,
    grade: grade,
  })

  return fetch(baseURL + "/check_safety", {
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
        throw new Error(`HTTP error status: ${response.status} ${response.statusText}`)
      }
      return response.json()
    })
    .then((data) => {
      return data.appropriate && data.safe
    })
    .catch((error) => {
      throw error
    })
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
        throw new Error(`HTTP error status: ${response.status} ${response.statusText}`)
      }
      return response.json()
    })
    .then((data) => data.story)
    .catch((error) => {
      throw error
    })
}

export const generateIllustration = async (story, abortSignal) => {
  let baseURL = getBaseURL()

  let payload = JSON.stringify({
    story: story,
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
      console.log("generateIllustration response", response)
      if (!response.ok) {
        throw new Error(`HTTP error status: ${response.status} ${response.statusText}`)
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
