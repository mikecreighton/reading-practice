import logo from "./logo.svg";
import "./App.scss";
import React, { useEffect, useRef, useState } from "react";
import StoryModal from "./components/StoryModal";
import InputForm from "./components/InputForm";

function App() {
  const [story, setStory] = useState(null);
  const inputFormRef = useRef();

  // This function is called when the server sends the entire story via a single response
  const handleStoryGenerated = (story) => {
    setStory(story);
  };

  // This function is called when the server sends a new story part via a streaming response
  const handleStoryPartReceived = (storyPart) => {
    setStory(storyPart);
  };

  // This function is called when the user closes the story modal and the animation has finished
  const handleStoryModalClosed = () => {
    setStory(null);
  };

  // This function is called when the user clicks the "Regenerate" button in the story modal
  const handleRegenerate = () => {
    inputFormRef.current.cancelRequest();
    inputFormRef.current.submitForm();
  };

  return (
    <div className="App">
      <div className="app-content">
        <InputForm
          ref={inputFormRef}
          onStoryPartReceived={handleStoryPartReceived}
          onStoryGenerated={handleStoryGenerated}
        />
        {story && (
          <StoryModal
            story={story}
            onRegenerate={handleRegenerate}
            onCloseComplete={handleStoryModalClosed}
            onCancelRequest={inputFormRef.current.cancelRequest}
          />
        )}
      </div>
    </div>
  );
}

export default App;
