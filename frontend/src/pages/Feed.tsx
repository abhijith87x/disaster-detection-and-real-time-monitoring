import { useEffect } from "react";
import "../style/Feed.css";

interface TileStyle extends React.CSSProperties {
    "--bg": string;
}

function Feed() {
    useEffect(() => {
    const hasSeenWelcome = localStorage.getItem("welcomeShown");

    if (!hasSeenWelcome) {
        alert(
           "Welcome to the Disaster Management System! Use the camera icon at the bottom right to upload real disaster images. Use the Demo button at the top right for testing and demonstration purposes, since real disaster incidents cannot be created for testing."
        );

        localStorage.setItem("welcomeShown", "true");
    }
    }, []);
    return (
        <div className="main-body">
            <div className="image">
                <div
                    className="tile"
                    style={{ "--bg": "#16213e" } as TileStyle}
                >
                    <i className="ti ti-map"></i>
                    <span>MAP</span>
                </div>

                <div
                    className="tile"
                    style={{ "--bg": "#0f3460" } as TileStyle}
                >
                    <i className="ti ti-satellite"></i>
                    <span>LIVE</span>
                </div>

                <div
                    className="tile"
                    style={{ "--bg": "#1a1a2e" } as TileStyle}
                >
                    <i className="ti ti-alert-circle"></i>
                    <span>ALERT</span>
                </div>

                <div
                    className="tile"
                    style={{ "--bg": "#0f3460" } as TileStyle}
                >
                    <i className="ti ti-camera"></i>
                    <span>REPORT</span>
                </div>

                <div
                    className="tile"
                    style={{ "--bg": "#16213e" } as TileStyle}
                >
                    <i className="ti ti-shield-check"></i>
                    <span>VERIFY</span>
                </div>

                <div
                    className="tile"
                    style={{ "--bg": "#1a1a2e" } as TileStyle}
                >
                    <i className="ti ti-users"></i>
                    <span>UNITE</span>
                </div>

                <div
                    className="tile"
                    style={{ "--bg": "#e94560" } as TileStyle}
                >
                    <i className="ti ti-send"></i>
                    <span>SEND</span>
                </div>
            </div>
        </div>
    );
}

export default Feed;