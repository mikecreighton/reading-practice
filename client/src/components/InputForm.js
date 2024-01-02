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
  const [humor, setHumorLevel] = useState(3);

  const submitForm = async () => {
    try {
      const response = await fetch(process.env.REACT_APP_API_URL + "/stream", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          words: words,
          subject: characterName,
          setting: setting,
          humor: humor + "",
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error status: ${response.statusText}`);
      } else {
        const reader = response.body.getReader();
        let story = "";
        let chunk;

        while ((chunk = await reader.read()) && !chunk.done) {
          story += new TextDecoder("utf-8").decode(chunk.value);
          props.onStoryPartReceived(story);
        }
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
    setHumorLevel(3);
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        <span class="prevent-wrap">
          Words to Include in the Story{" "}
          <span className="helper">(comma-separated)</span>
        </span>
        <input
          type="text"
          value={words}
          onChange={(e) => setWords(e.target.value)}
        />
      </label>
      <label>
        The Story&rsquo;s Main Character
        <input
          type="text"
          value={characterName}
          onChange={(e) => setCharacterName(e.target.value)}
        />
      </label>
      <label>
        Where the Story Takes Place
        <input
          type="text"
          value={setting}
          onChange={(e) => setSetting(e.target.value)}
        />
      </label>
      <label>
        Humor Level
        <input
          type="range"
          min="1"
          max="10"
          defaultValue={humor}
          value={humor}
          onChange={(e) => setHumorLevel(e.target.value)}
          className="slider"
        />
      </label>
      <div className="buttons-container">
        <button class="button-labeled" type="submit">
          Generate Story
        </button>
        <button class="button-labeled" type="reset" onClick={handleReset}>
          Reset
        </button>
      </div>
    </form>
  );
});

export default InputForm;
