import { GoogleMap, LoadScript, Marker } from "@react-google-maps/api";
import { Loader } from "react-loaders"
import {
  BsSearch,
  BsFillChatDotsFill,
  BsGift,
  BsFillCaretLeftFill,
  BsPersonFill,
} from "react-icons/bs";
import { MdClose } from "react-icons/md";
import { NavLink } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { useState } from "react";

import Modal from "../Modal/Modal";

import * as modalActions from "../../store/reducers/modal";
import * as sessionActions from "../../store/reducers/session";

import "loaders.css/src/animations/ball-scale.scss";
import "./Navbar.css";

const Navbar = () => {
  // Hooks
  const sessionUser = useSelector(s => s.session.user);
  const dispatch = useDispatch();

  // Component state
  const profilePictureSrc64 = `/f/profile_${sessionUser.id}_64p.jpg`;

  // Event handlers
  const toggleUserMenu = (evt) => {
    evt.preventDefault();
    dispatch(modalActions.setModal({
      component: <UserMenu
        onClearCallback={toggleUserMenu} />,
      clearOnClick: true,
    }))
  }

  return (
    <div className="navbar-viewport-container">
      <div className="navbar">
        <div className="navbar__page-width">
          <div className="navbar__brand"></div>
          <div className="navbar__links">
            <NavLink exact to="/" activeClassName="active" className="browse">
              <BsGift />
            </NavLink>
            <NavLink to="/search" activeClassName="active" className="search">
              <BsSearch />
            </NavLink>
            <NavLink to="/messages" activeClassName="active" className="chat">
              <BsFillChatDotsFill />
            </NavLink>
            <a href="/#" className="profile" onClick={toggleUserMenu}>
              <img src={profilePictureSrc64} alt="" />
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}

const UserMenu = ({ onClearCallback }) => {
  // Hooks
  const sessionUser = useSelector(s => s.session.user);
  const dispatch = useDispatch();

  // Component state
  const [mapLoaded, setMapLoaded] = useState(null);
  const googleMapsAPIKey = process.env.REACT_APP_GOOGLE_API_KEY;
  const googleMapsDefaultCenter = {
    lat: parseFloat(sessionUser.coordLat),
    lng: parseFloat(sessionUser.coordLong),
  };
  const googleMapsUserMenuStyles = {
    height: "12rem",
    width: "100%",
  }
  const googleMapsOptions = {
    draggable: false,
    disableDefaultUI: true,
  }
  const profilePictureSrc128 = `/f/profile_${sessionUser.id}_128p.jpg`;

  // Event handlers
  const onGoogleMapsMount = (evt) => {
    dispatch(sessionActions.patchSessionGeolocation());
    setMapLoaded(true);
  }
  const onGoogleMapsUnmount = () => {
    setMapLoaded(false);
  }
  const logout = (evt) => {
    evt.preventDefault()
    dispatch(sessionActions.logoutSessionUser());
  }
  const clearModal = (evt) => {
    dispatch(modalActions.clearModal());
  }

  return (
    <Modal>
      <div className="user-menu">
        <MdClose className="close" onClick={clearModal} />
        <div className="user-menu__header">
          <img src={profilePictureSrc128} alt="" />
          <p className="name">{sessionUser.firstName} {sessionUser.lastName}</p>
          <p className="email">{sessionUser.email}</p>
        </div>
        <div className="user-menu__location">
          {!mapLoaded ?
            <div className="map-preloader">
              <Loader
                type="ball-scale"
                color="#555555" />
            </div> : ""
          }
          <LoadScript googleMapsApiKey={googleMapsAPIKey}>
            <GoogleMap
              onLoad={onGoogleMapsMount}
              onUnmount={onGoogleMapsUnmount}
              zoom={13}
              mapContainerStyle={googleMapsUserMenuStyles}
              center={googleMapsDefaultCenter}
              options={googleMapsOptions}>
              <Marker position={googleMapsDefaultCenter} />
            </GoogleMap>
          </LoadScript>
        </div>
        <ul className="user-menu__menu">
          <li className="edit-profile">
            <a href="/#" onClick={null} className="inactive">
              <BsPersonFill />
              <p>Edit Profile</p>
            </a>
          </li>
          <li className="logout">
            <a href="/#" onClick={logout}>
              <BsFillCaretLeftFill />
              <p>Logout</p>
            </a>
          </li>
        </ul>
      </div>
    </Modal>
  )
}

export default Navbar;
