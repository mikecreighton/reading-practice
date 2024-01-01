import logo from './logo.svg';
import './App.scss';
import React, { useEffect, useState } from 'react';
import StoryModal from './components/StoryModal';
import InputForm from './components/InputForm';

function App() {
  const [story, setStory] = useState(null);

  const handleStoryGenerated = (story) => {
    setStory(story);
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>Story Generator</h1>
      </header>
      <div>
        <InputForm onStoryGenerated={handleStoryGenerated} />
        {story && <StoryModal story={story} onClose={() => setStory(null)} />}
      </div>
    </div>
  );
}

export default App;
