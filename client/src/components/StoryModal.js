import React from "react";
import "./StoryModal.scss";

function StoryModal({ story, onRegenerate, onClose }) {
  return (
    <div className="modal">
      <div class="modal-content">
        <p>{story}</p>
        <button onClick={onClose}>Close</button>
        <button onClick={onRegenerate}>Regenerate</button>
      </div>
    </div>
  );
}

export default StoryModal;
