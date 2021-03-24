import { Loader } from "react-loaders";
import { useState } from "react"

import "loaders.css/src/animations/ball-scale.scss";
import "./ImagePreload.css";

const ImagePreload = ({ src }) => {
  // Component state
  const FETCHING = "fetching";
  const SHOW = "show";
  const ERROR = "error";
  const [imgLoaded, setImgLoaded] = useState(FETCHING);

  // Event handlers
  const onImageLoad = (evt) => {
    if (evt.type === "error") setImgLoaded(ERROR);
    else setImgLoaded(SHOW);
  }

  return (
    <div className="img-pre">
      <div className={"preloader " + imgLoaded}>
        {imgLoaded === ERROR ?
          <span>!</span> : ""
        }
      </div>
      <img
        src={src}
        alt=""
        className={imgLoaded}
        onLoad={onImageLoad}
        onError={onImageLoad} />
    </div>
  );
}

export default ImagePreload;
