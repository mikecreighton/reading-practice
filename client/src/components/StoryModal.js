import { React, useEffect } from "react";
import { gsap, Power4 } from "gsap";
import "./StoryModal.scss";

function StoryModal({ story, onRegenerate, onClose }) {
  useEffect(() => {
    gsap.to(".modal", { duration: 0.5, y: "0%", ease: Power4.easeOut });
  }, []);

  const handleClose = (event) => {
    event.preventDefault();
    gsap.to(".modal", { duration: 0.5, y: "100%", ease: Power4.easeInOut, onComplete: onClose });
  };

  return (
    <div className="modal">
      <div className="modal-content">
        <p>{story}</p>
        <button className="modal-close-button" onClick={handleClose}>
          &#x2715;
        </button>
        <button onClick={onRegenerate}>Regenerate</button>
      </div>
    </div>
  );
}

export default StoryModal;
