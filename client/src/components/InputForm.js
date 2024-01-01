import React, {
  useState,
  useRef,
  useImperativeHandle,
  forwardRef,
} from "react";
import "./InputForm.scss";

const InputForm = forwardRef((props, ref) => {
  const [words, setWords] = useState("");
  const [characterName, setCharacterName] = useState("");
  const [setting, setSetting] = useState("");

  const submitForm = async () => {
    try {
      const response = await fetch(
        process.env.REACT_APP_API_URL + "/generate",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            words: words,
            subject: characterName,
            setting: setting,
          }),
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error status: ${response.statusText}`);
      } else {
        const data = await response.json();
        const story = data.story;
        props.onStoryGenerated(story);
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  useImperativeHandle(ref, () => ({
    submitForm: submitForm,
  }));

  const handleSubmit = (event) => {
    event.preventDefault();
    submitForm(event);
  };

  const handleReset = (event) => {
    event.preventDefault();
    setWords("");
    setCharacterName("");
    setSetting("");
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Words to include in the story:
        <input
          type="text"
          value={words}
          onChange={(e) => setWords(e.target.value)}
        />
      </label>
      <label>
        The main character:
        <input
          type="text"
          value={characterName}
          onChange={(e) => setCharacterName(e.target.value)}
        />
      </label>
      <label>
        Setting for the story:
        <input
          type="text"
          value={setting}
          onChange={(e) => setSetting(e.target.value)}
        />
      </label>
      <button type="submit">Generate Story</button>
      <button type="reset" onClick={handleReset}>
        Reset
      </button>
    </form>
  );
});

export default InputForm;
