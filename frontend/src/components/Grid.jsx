import "../style/Grid.css";
import DisasterCard from "./DisasterCard";
import { useEffect, useState } from "react";
import { checkuser } from "../checkuser/checkuser.js";
import socket from "../socket_server/SocketServer.js";

function Grid() {

    const [reports, setReports] = useState([]);

    const [page, setPage] = useState(1);

    const [userActionMap, setUserActionMap] = useState({});

    const [currentUserId, setCurrentUserId] = useState("");

    const [loading, setLoading] = useState(false);


    // =================================
    // FETCH REPORTS
    // =================================

    async function loadReports() {

        // Prevent multiple requests
        if (loading) {
            return;
        }

        setLoading(true);

        try {

            // =========================
            // 1. FETCH REPORTS
            // =========================

            const res = await fetch(
                `/feed/reports/latest?page=${page}`
            );

            const newReports = await res.json();


            // No more reports
            if (newReports.length === 0) {
                return;
            }


            // =========================
            // 2. CHECK CURRENT USER
            // =========================

            const response = await checkuser();

            let userId = "";


            if (response.ok) {

                const user = await response.json();


                if (user) {

                    userId = user.id;

                    setCurrentUserId(user.id);


                    // =========================
                    // 3. FETCH USER ACTIONS
                    // =========================

                    const actionResponse = await fetch(
                        `/feed/card/action?currentUser=${user.id}`
                    );


                    if (actionResponse.ok) {

                        const actions =
                            await actionResponse.json();


                        const actionMap = {};


                        actions.forEach((action) => {

                            actionMap[action.card_id] = action;

                        });


                        setUserActionMap(actionMap);

                    }

                }

            }


            // =========================
            // 4. PREVENT DUPLICATE REPORTS
            // =========================

            setReports((oldReports) => {


                // Store all existing image IDs
                const existingIds = new Set(

                    oldReports.map(
                        (report) => report.image_id
                    )

                );


                // Keep only new reports
                const uniqueReports = newReports.filter(

                    (report) =>
                        !existingIds.has(
                            report.image_id
                        )

                );


                // Add only unique reports
                return [

                    ...oldReports,

                    ...uniqueReports

                ];

            });


            // =========================
            // 5. NEXT PAGE
            // =========================

            setPage(
                (oldPage) => oldPage + 1
            );


        } finally {

            setLoading(false);

        }

    }


    // =================================
    // INITIAL LOAD
    // =================================

    useEffect(() => {

        loadReports();

    }, []);


    // =================================
    // SCROLL
    // =================================

    useEffect(() => {


        function handleScroll() {


            const nearBottom =

                window.innerHeight +

                window.scrollY >=

                document.body.offsetHeight - 100;


            if (nearBottom) {

                loadReports();

            }

        }


        window.addEventListener(

            "scroll",

            handleScroll

        );


        return () => {


            window.removeEventListener(

                "scroll",

                handleScroll

            );

        };


    }, [loading]);


    // =================================
    // RENDER ALL REPORTS
    // =================================
    
    function handleNewReport(report) {
        setReports((oldReports) => {
            const exist = oldReports.some(
                (oldReports) => 
                    oldReports.image_id === report.card_id
            );

            if (exist) {
                return oldReports;
            }
            
            return [
                report,
                ...oldReports
            ];
        });
    }
    
    function handleRemoveReport(report) {
        setReports((oldReports) => 
            oldReports.filter(
                (oldReport) => 
                oldReport.image_id !== report
            )
        );
    }

    function handleStatusUpdate(data) {
        setReports((oldReports) => 
            oldReports.map(
                (report) =>
                    report.image_id === data.card_id ? {
                        ...report,
                        status : data.status
                    }
                    :report
            )
        )
    }

    function handleDescriptionUpdate(data) {
        setReports((oldReports) => 
            oldReports.map(
                (report) =>
                    report.image_id === data.card_id ? {
                        ...report,
                        description : data.description
                    }
                    : report
            )
        )
    }

useEffect(() =>{
        
    socket.on(
        "new_report",
        handleNewReport
    );

    socket.on(
        "remove_report",
        handleRemoveReport
    );

    socket.on(
        "status_update",
        handleStatusUpdate
    );

    socket.on(
        "update_description",
        handleDescriptionUpdate
    );

    return ()=> {
        socket.off(
        "new_report",
         handleNewReport
    );

    socket.off(
        "remove_report",
        handleRemoveReport
    );

    socket.off(
        "status_update",
        handleStatusUpdate
    );

    socket.off(
        "update_discription",
        handleDescriptionUpdate
    );

    };

},[])

    return (

        <div

            className="cards-grid"

            id="disaster-feed"

        >


            {reports.map((report) => {


                // Find this card's user action
                const userActions =

                    userActionMap[
                        report.image_id
                    ];


                // Check if current user owns this report
                const canDelete =

                    report.user_id ===
                    currentUserId;


                return (

                    <DisasterCard

                        key={report.image_id}

                        report={report}

                        user_actions={userActions}

                        canDelete={canDelete}

                    />

                );

            })}


        </div>

    );

}


export default Grid;