import { useEffect, useRef, useState } from "react";
import { useSelector } from "react-redux";

import "./Search.css";
import { searchConnections } from "./_searches";

const Search = ({ filter, prompt: prm, obscurityCallback, ItemComponent }) => {
  // default message in search box if none is provided
  const prompt = prm ? prm : "Start typing to search...";

  // hooks
  const searchRef = useRef(null);
  const connections = useSelector(s => s.connections);

  // component persistent state
  const [term, setTerm] = useState("");
  const [results, setResults] = useState([]);

  // ******************************************************
  // side effect focuses search input on render
  useEffect(() => {
    const cur = searchRef.current;
    cur.focus();
  }, []);

  // ******************************************************
  // side effect mounts data to search box
  useEffect(() => {
    if (term.length && filter) {
      switch (filter) {
        case "connections":
          setResults(searchConnections(connections, term));
      }
    }
  }, [term, connections]);

  // ******************************************************
  // event handler calls obscurity callback when dark area
  // is clicked
  const onObscurityClick = (evt) => {
    obscurityCallback();
  }

  // ******************************************************
  // event handler calls actions once an item is clicked
  const onItemClick = (evt) => {
    obscurityCallback();
  }
  // ******************************************************
  // event handler prevents propagation from the search box
  // to the dark area
  const onSearchBoxClick = (evt) => evt.stopPropagation();

  return (
    <div
      className="search page-grid"
      onClick={onObscurityClick}>
      <div onClick={onSearchBoxClick}>
        <input
          type="text"
          name="search"
          ref={searchRef}
          id="searchComponent"
          placeholder="Search"
          value={term}
          autoComplete="chrome-off"
          onChange={(e) => setTerm(e.target.value)} />
        <div>
          {!term ?
            <span>{prompt}</span> : 
            <ul>
              {results.map((r, i) => (
                <div key={"search-result-" + i} onClick={onItemClick}>
                  <ItemComponent resultObject={r} />
                </div>
              ))}
            </ul>
          }
        </div>
      </div>
    </div>
  )
}

export default Search;
