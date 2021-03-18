import './Modal.css';

const Modal = ({ children, zIndex, clearFunction, clearOnClick }) => {

  // Event handlers
  const clearModal = (evt) => {
    if (clearOnClick) {
      clearFunction(evt)
    }
  }
  const stopPropagation = (evt) => {
    evt.stopPropagation();
  }

  return (
    <div
      className="modal"
      style={{zIndex}}
      onClick={clearModal}>
      <div
        className="modal__center"
        onClick={stopPropagation}>
        {children}
      </div>
    </div>
  )
}

export default Modal;
