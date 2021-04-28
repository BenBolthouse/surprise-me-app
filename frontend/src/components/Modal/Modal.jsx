import { useDispatch, useSelector } from "react-redux";

import * as modalActions from "../../store/reducers/modal";

import './Modal.css';

const Modal = ({ children }) => {
  // Hooks
  const modalClearOnClick = useSelector(s => s.modal.clearOnClick);
  const dispatch = useDispatch();
  
  // Event handlers
  const stopPropagation = (evt) => {
    evt.stopPropagation();
  }
  const clear = (evt) => {
    if (modalClearOnClick) {
      dispatch(modalActions.clearModal());
    }
  }

  return (
    <div className="modal" onClick={clear}>
      <div
        className="modal__center"
        onClick={stopPropagation}>
        {children}
      </div>
    </div>
  )
}

export default Modal;
