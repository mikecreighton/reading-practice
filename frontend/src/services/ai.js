export const generateStory = async (words, characterName, setting, humor, abortSignal) => {
  let baseURL = import.meta.env.VITE_API_URL ? import.meta.env.VITE_API_URL : ""

  // Strip out any trailing slashes from the base URL.
  baseURL = baseURL.replace(/\/$/, '')

  let payload = JSON.stringify({
    words: words,
    subject: characterName,
    setting: setting,
    humor: humor + "",
  })

  console.log("payload", payload)

  return fetch(baseURL + "/generate_story", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Accept": "application/json",
    },
    body: payload,
    signal: abortSignal,
  })
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error status: ${response.status} ${response.statusText}`);
      }
      return response.json();
    })
    .then(data => data.story)
    .catch(error => {
      throw error;
    })
}
