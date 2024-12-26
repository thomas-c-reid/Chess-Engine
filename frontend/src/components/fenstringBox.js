import React from "react";
import "../css/fenstring.css";

function FenStringBox({fenstring}) {
  return (
    <div className="fen-box">
      <div className="fen-string" onClick={() => navigator.clipboard.writeText(fenstring)}>
        {fenstring}
      </div>
    </div>
  );
}

export default FenStringBox;
