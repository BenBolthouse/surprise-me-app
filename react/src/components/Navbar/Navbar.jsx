import {
  BsSearch,
  BsFillChatDotsFill,
  BsGift,
  BsFillCaretLeftFill
} from "react-icons/bs";
import { MdClose } from "react-icons/md";
import { NavLink } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { useState } from "react";

import Modal from "../Modal/Modal";

import * as sessionActions from "../../store/reducers/session";

import "./Navbar.css";

const Navbar = () => {
  // Hooks
  const sessionUser = useSelector(s => s.session.user);
  const dispatch = useDispatch();

  // Component state
  const [userMenuIsOpen, setUserMenuIsOpen] = useState(false);

  const profilePictureSrc64 = `/f/profile_${sessionUser.id}_64p.jpg`;
  const profilePictureSrc128 = `/f/profile_${sessionUser.id}_128p.jpg`;

  const logout = (evt) => {
    evt.preventDefault()
    dispatch(sessionActions.logoutSessionUser());
  }
  const toggleUserMenu = (evt) => {
    evt.preventDefault();
    setUserMenuIsOpen(!userMenuIsOpen);
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
              <img src={profilePictureSrc64} />
            </a>
          </div>
          {userMenuIsOpen ?
            <Modal
              zIndex="901"
              clearFunction={toggleUserMenu}
              clearOnClick={true}>
              <div className="user-menu">
                <MdClose className="close" onClick={toggleUserMenu} />
                <div className="user-menu__header">
                  <img src={profilePictureSrc128} />
                  <p className="name">{sessionUser.firstName} {sessionUser.lastName}</p>
                  <p className="email">{sessionUser.email}</p>
                </div>
                <ul className="user-menu__menu">
                  <li className="logout">
                    <a href="#" onClick={logout}>
                      <BsFillCaretLeftFill />
                      <p>Logout</p>
                    </a>
                  </li>
                </ul>
              </div>
            </Modal> : ""
          }
        </div>
      </div>
    </div>
  )
}

export default Navbar;
