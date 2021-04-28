import { GoogleMap, LoadScript, Marker } from "@react-google-maps/api";
import { Loader } from "react-loaders";

import { BsFillChatSquareFill as ChatIcon } from "react-icons/bs";
import { BsFillHouseDoorFill as HomeIcon } from "react-icons/bs";
import { BsPersonFill as ProfileIcon } from "react-icons/bs";
import { BsFillCaretLeftFill as LogoutIcon } from "react-icons/bs";
import { BsX as CloseIcon } from "react-icons/bs";

import { NavLink } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { useEffect, useState } from "react";

import Modal from "../Modal/Modal";

import * as modalActions from "../../store/reducers/modal";
import * as sessionActions from "../../store/reducers/session";

import "loaders.css/src/animations/ball-scale.scss";
import "./Navbar.css";
import ImagePreload from "../ImagePreload/ImagePreload";

const Navbar = () => {
  // Hooks
  const sessionUser = useSelector(s => s.session.user);
  const notifications = useSelector(s => s.connections.notifications);
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
        <div className="page-grid">
          <div className="links">
            <NavLink exact to="/" activeClassName="active" className="browse">
              <HomeIcon />
            </NavLink>
            <NavLink to="/messages" activeClassName="active" className="chat">
              <ChatIcon />
              {notifications && notifications.length ?
                <div className="notifications">
                  {notifications.length}
                </div> : ""
              }
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

const UserMenu = () => {
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
    clearModal();
  }
  const clearModal = (evt) => {
    dispatch(modalActions.clearModal());
  }

  return (
    <Modal>
      <div className="user-menu">
        <CloseIcon className="close" onClick={clearModal} />
        <div className="top">
          <ImagePreload src={profilePictureSrc128} />
          <p className="name">{sessionUser.firstName} {sessionUser.lastName}</p>
          <p className="email">{sessionUser.email}</p>
        </div>
        <div className="location">
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
        <ul className="menu">
          <li className="edit-profile">
            <a href="/#" onClick={null} className="inactive">
              <ProfileIcon />
              <p>Edit Profile</p>
            </a>
          </li>
          <li className="logout">
            <a href="/#" onClick={logout}>
              <LogoutIcon />
              <p>Logout</p>
            </a>
          </li>
        </ul>
      </div>
    </Modal>
  )
}

export default Navbar;
