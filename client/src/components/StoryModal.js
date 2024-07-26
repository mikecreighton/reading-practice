import { React, useEffect } from "react";
import { gsap, Power4 } from "gsap";
import "./StoryModal.scss";

// StoryModal component displays the generated story and handles modal actions
function StoryModal({ story, onRegenerate, onCloseComplete, onCancelRequest }) {
    
  // This effect is called when the story modal is first rendered and kicks off the opening animation
  // Effect to animate the modal when it is first rendered
  useEffect(() => {
    gsap.to(".modal", { duration: 0.5, y: "0%", ease: Power4.easeOut });
  }, []);

  // This function is called when the user clicks the "X" button in the story modal which kicks off closing animation
  // Handle the close request for the modal
  const handleCloseRequest = (event) => {
    event.preventDefault();
    onCancelRequest();
    gsap.to(".modal", {
      duration: 0.5,
      y: "100%",
      ease: Power4.easeInOut,
      onComplete: onCloseComplete,
    });
  };

  return (
    <div className="modal">
      <div className="modal-content">
        <p>{story}</p>
        <button className="modal-close-button" onClick={handleCloseRequest}>
          &#x2715;
        </button>
        <button
          className="button-labeled modal-regenerate-button"
          onClick={onRegenerate}
        >
          Regenerate
        </button>
      </div>
    </div>
  );
}

export default StoryModal;
