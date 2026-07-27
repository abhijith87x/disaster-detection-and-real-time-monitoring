import "../style/Feed.css";

function Feed() {
    return (

        <div className="main-body">
        <div className="image">
            <div className="tile" style={{ "--bg": "#16213e" }}>
                <i className="ti ti-map"></i>
                <span>MAP</span>
            </div>

            <div className="tile" style={{ "--bg": "#0f3460" }}>
                <i className="ti ti-satellite"></i>
                <span>LIVE</span>
            </div>

            <div className="tile" style={{ "--bg": "#1a1a2e" }}>
                <i className="ti ti-alert-circle"></i>
                <span>ALERT</span>
            </div>

            <div className="tile" style={{ "--bg": "#0f3460" }}>
                <i className="ti ti-camera"></i>
                <span>REPORT</span>
            </div>

            <div className="tile" style={{ "--bg": "#16213e" }}>
                <i className="ti ti-shield-check"></i>
                <span>VERIFY</span>
            </div>

            <div className="tile" style={{ "--bg": "#1a1a2e" }}>
                <i className="ti ti-users"></i>
                <span>UNITE</span>
            </div>

            <div className="tile" style={{ "--bg": "#e94560" }}>
                <i className="ti ti-send"></i>
                <span>SEND</span>
            </div>
        </div>
        </div>
    );
}

export default Feed;