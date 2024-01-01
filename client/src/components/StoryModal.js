import React from 'react';

function StoryModal({ story, onClose }) {
 return (
   <div className="modal">
     <p>{story}</p>
     <button onClick={onClose}>Close</button>
   </div>
 );
}

export default StoryModal;
