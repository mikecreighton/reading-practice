import logo from './logo.svg';
import './App.scss';
import React, { useEffect, useRef, useState } from 'react';
import StoryModal from './components/StoryModal';
import InputForm from './components/InputForm';

function App() {
  const [story, setStory] = useState(null);
  const inputFormRef = useRef();

  const handleStoryGenerated = (story) => {
    setStory(story);
  }

  const handleStoryPartReceived = (storyPart) => {
    setStory(storyPart);
  }

  const handleStoryModalClose = () => {
    setStory(null);
  }

  const handleRegenerate = () => {
    inputFormRef.current.submitForm();
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>Story Generator</h1>
      </header>
      <div>
        <InputForm ref={inputFormRef} onStoryPartReceived={handleStoryPartReceived} onStoryGenerated={handleStoryGenerated} />
        {story && <StoryModal story={story} onRegenerate={handleRegenerate} onCloseComplete={handleStoryModalClose} />}
      </div>
    </div>
  );
}

export default App;
