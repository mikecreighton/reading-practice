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

  const handleRegenerate = () => {
    console.log("Regenerate");
    inputFormRef.current.submitForm();
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>Story Generator</h1>
      </header>
      <div>
        <InputForm ref={inputFormRef} onStoryGenerated={handleStoryGenerated} />
        {story && <StoryModal story={story} onRegenerate={handleRegenerate} onClose={() => setStory(null)} />}
      </div>
    </div>
  );
}

export default App;
