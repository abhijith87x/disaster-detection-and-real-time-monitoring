import { checkuser } from "../checkuser";
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import '../style/CardActions.css';
import type { Report } from "../types/Report";

interface CardActionProps {
    report: Pick<Report, "image_id" | "latitude" | "longitude">;
    user_actions?: UserActions;
    canDelete: boolean;
}

interface UserActions {
   reaction?: "LIKE" | "DISLIKE" | null;
   reported?: "TRUE" | "FALSE"
}


interface User {
    id: number;
}

function CardActions({ report, user_actions, canDelete }: CardActionProps) {
    const navigate = useNavigate();

    // Existing reaction data from backend
    const reaction = user_actions?.reaction;
    const reportedFromDB = user_actions?.reported;

    // Local UI states
    const [like, setLike] = useState<boolean>(reaction === "LIKE");
    const [dislike, setDislike] = useState<boolean>(reaction === "DISLIKE");

    const [dislikePopup, setDislikePopup] = useState<boolean>(false);
    const [selectedType, setSelectedType] = useState<string>("");

    const [isReported, setIsReported] = useState<boolean>(
        reportedFromDB === "TRUE"
    );

    const [deleteMenu, setDeleteMenu] = useState<boolean>(false);
    console.log("deletemenu",deleteMenu)
    const burst = (
        <span className="burst-wrap">
            <span className="b b1"></span>
            <span className="b b2"></span>
            <span className="b b3"></span>
            <span className="b b4"></span>
            <span className="b b5"></span>
            <span className="b b6"></span>
        </span>
    );

    // -------------------------
    // LIKE
    // -------------------------

    async function handleLike(): Promise<void> {
        const response = await checkuser();

        if (!response.ok) {
            navigate("/login-page");
            return;
        }

        const user: User = await response.json();

        if (!user) {
            navigate("/login-page");
            return;
        }

        const currentUserId = user.id;

        // If currently disliked, remove dislike
        if (dislike) {
            setDislike(false);
        }

        // Calculate next value BEFORE changing state
        const nextLike = !like;

        // Update UI immediately
        setLike(nextLike);

        // Send the new value to backend
        await fetch(
            `/api/disaster/user/like/update?current_user=${currentUserId}&card_id=${report.image_id}&like=${nextLike}`,
            {
                method: "POST",
                credentials: "include",
            }
        );
    }

    // -------------------------
    // DISLIKE
    // -------------------------

    const dislikeReasons: string[] = [
        "Flood",
        "Landslide",
        "Earthquake",
        "Wildfire",
        "Tsunami",
    ];

    async function handleDislike(): Promise<void> {
        const response = await checkuser();

        if (!response.ok) {
            navigate("/login-page");
            return;
        }

        const user: User = await response.json();

        if (!user) {
            navigate("/login-page");
            return;
        }

        // If currently liked, remove like
        if (like) {
            setLike(false);
        }

        const nextDislike = !dislike;

        setDislike(nextDislike);

        // Open popup only when turning dislike ON
        if (nextDislike) {
            setDislikePopup(true);
        }
    }

    // -------------------------
    // CONFIRM DISLIKE
    // -------------------------

    async function confirmDislike(): Promise<void> {
        const response = await checkuser();

        if (!response.ok) {
            navigate("/login-page");
            return;
        }

        const user: User = await response.json();

        if (!user) {
            navigate("/login-page");
            return;
        }

        const currentUserId = user.id;

        await fetch(
            `/api/disaster/user/dislike/update?current_user=${currentUserId}&card_id=${report.image_id}&dislike=${dislike}&type=${selectedType}`,
            {
                method: "POST",
                credentials: "include",
            }
        );

        setDislikePopup(false);
    }

    // -------------------------
    // LOCATION
    // -------------------------

    function openLocation(
        latitude: number, 
        longitude: number
    ): void {
        window.open(
            `https://www.google.com/maps?q=${latitude},${longitude}`,
            "_blank"
        );
    }

    // -------------------------
    // REPORT
    // -------------------------

    async function handleReport(): Promise<void> {
        const response = await checkuser();

        if (!response.ok) {
            navigate("/login-page");
            return;
        }

        const user: User = await response.json();

        if (!user) {
            navigate("/login-page");
            return;
        }

        const currentUserId = user.id;

        // Calculate the next value first
        const nextReported = !isReported;

        // Update UI
        setIsReported(nextReported);

        // Send the updated value to backend
        await fetch(
            `/api/disaster/user/report/update?current_user=${currentUserId}&card_id=${report.image_id}&report=${nextReported}`,
            {
                method: "POST",
                credentials: "include",
            }
        );
    }

    // -------------------------
    // DELETE
    // -------------------------

    async function deleteCard(): Promise<void> {
        const response = await checkuser();

        if (!response.ok) {
            navigate("/login-page");
            return;
        }

        const user: User = await response.json();

        if (!user) {
            navigate("/login-page");
            return;
        }

        const currentUserId = user.id;

        const responseDelete = await fetch(
            `/api/disaster/user/reports/delete?card_id=${report.image_id}&currentUserId=${currentUserId}`,
            {
                method: "DELETE",
                credentials: "include",
            }
        );

        const data: { success: boolean} = await responseDelete.json();

        if (data.success) {
            // You can later call a parent function here
            // to remove this card from the reports state.
            console.log("Card deleted:", report.image_id);

            setDeleteMenu(false);
        }
    }


    return (
        <div className="cacts">

            {/* LIKE BUTTON */}
            <button
                className={`abtn ${like ? "lk-on" : ""}`}
                onClick={handleLike}
            >
                {burst}

                <i className="ti ti-thumb-up"></i>
            </button>


            {/* DISLIKE BUTTON */}
            <button
                className={`abtn ${dislike ? "dk-on" : ""}`}
                onClick={handleDislike}
                aria-label="Doubt"
            >
                {burst}

                <i className="ti ti-thumb-down"></i>
            </button>


            {/* DISLIKE POPUP */}
            {dislikePopup && (
                <div className="dislike-overlay">

                    <div className="dislike-box">

                        <h3 className="dislike-title">
                            What type of disaster is this?
                        </h3>


                        <div className="dislike-options">

                            {dislikeReasons.map((reason, index) => (

                                <label
                                    className="dislike-option"
                                    key={reason}
                                >

                                    <input
                                        type="radio"
                                        name={`dislikeReason-${report.image_id}`}
                                        value={reason}
                                        defaultChecked={index === 0}
                                        onChange={(
                                            event: React.ChangeEvent<HTMLInputElement>
                                        ) => {
                                            setSelectedType(
                                                event.target.value
                                            );
                                        }}
                                    />

                                    <span>
                                        {reason}
                                    </span>

                                </label>

                            ))}

                        </div>


                        <div className="dislike-actions">

                            {/* CANCEL */}
                            <button
                                className="dislike-cancel"
                                onClick={() => {
                                    setDislikePopup(false);
                                    setDislike(false);
                                }}
                            >
                                Cancel
                            </button>


                            {/* SUBMIT */}
                            <button
                                className="dislike-submit"
                                onClick={confirmDislike}
                            >
                                Submit
                            </button>

                        </div>

                    </div>

                </div>
            )}


            {/* LOCATION BUTTON */}
            <button
                className="loc-btn"
                onClick={() =>
                    openLocation(
                        report.latitude,
                        report.longitude
                    )
                }
                aria-label="Location"
            >
                <i className="ti ti-map-pin"></i>
            </button>
            
            <div className="sp"></div>

            {/* REPORT BUTTON */}
            <button
                className={`rpt-btn ${
                    isReported ? "reported" : ""
                }`}
                onClick={handleReport}
            >
                {isReported ? "Reported" : "Report"}
            </button>


            {/* THREE DOT DELETE MENU */}
            {canDelete && (

                <div className="tdwrap">

                    <button
                        className="tdbtn"
                        onClick={() =>
                            setDeleteMenu(!deleteMenu)
                        }
                        aria-label="More options"
                    >
                        <i className="ti ti-dots-vertical"></i>
                    </button>


                    {deleteMenu && (
                       
                        <div className="ddrop">

                            <button
                                onClick={deleteCard}
                            >
                                <i className="ti ti-trash"></i>

                                Delete
                            </button>

                        </div>

                    )}

                </div>

            )}

        </div>
    );
}

export default CardActions;