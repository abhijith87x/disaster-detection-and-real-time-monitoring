import "../style/Grid.css";
import DisasterCard from "./DisasterCard";
import { useEffect, useState } from "react";
import { checkuser } from "../checkuser";
import socket from "../socket_server/SocketServer.js";
import type { Report } from "../types/Report";

interface UserActions {
    reaction?: "LIKE" | "DISLIKE" | null;
    reported?: "TRUE" | "FALSE";
}

interface ActionResponse {
    card_id: number;
    reaction?: "LIKE" | "DISLIKE" | null;
    reported?: "TRUE" | "FALSE";
}

interface User {
    id: number;
}

interface NewReport {
    card_id: number;
    image_id: number;
    image_path: string;
    latitude: number;
    longitude: number;
    status: string;
    description: string;
    user_id: number;
}

interface StatusUpdate {
    card_id: number;
    status: string;
}

interface DescriptionUpdate {
    card_id: number;
    description: string;
}

function Grid() {

    const [reports, setReports] = useState<Report[]>([]);

    const [page, setPage] = useState<number>(1);

    const [userActionMap, setUserActionMap] = useState<
        Record<number, UserActions>
    >({});

    const [currentUserId, setCurrentUserId] = useState<number | null>(null);

    const [loading, setLoading] = useState<boolean>(false);


    async function loadReports(): Promise<void> {

        if (loading) {
            return;
        }

        setLoading(true);

        try {

            const res = await fetch(
                `/feed/reports/latest?page=${page}`
            );

            const newReports: Report[] = await res.json();

            if (newReports.length === 0) {
                return;
            }

            const response = await checkuser();

            if (response.ok) {

                const user: User = await response.json();

                if (user) {

                    setCurrentUserId(user.id);

                    const actionResponse = await fetch(
                        `/feed/card/action?currentUser=${user.id}`
                    );

                    if (actionResponse.ok) {

                        const actions: ActionResponse[] =
                            await actionResponse.json();

                        const actionMap: Record<number, UserActions> = {};

                        actions.forEach((action) => {

                            actionMap[action.card_id] = {
                                reaction: action.reaction,
                                reported: action.reported
                            };

                        });

                        setUserActionMap(actionMap);
                    }
                }
            }

            setReports((oldReports) => {

                const existingIds = new Set(
                    oldReports.map(
                        (report) => report.image_id
                    )
                );

                const uniqueReports = newReports.filter(
                    (report) =>
                        !existingIds.has(report.image_id)
                );

                return [
                    ...oldReports,
                    ...uniqueReports
                ];
            });

            setPage(
                (oldPage) => oldPage + 1
            );

        } finally {

            setLoading(false);

        }
    }


    useEffect(() => {

        loadReports();

    }, []);


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


    function handleNewReport(report: NewReport): void {
        console.log("Received new report:", report);
        setReports((oldReports) => {

            const exists = oldReports.some(
                (oldReport) =>
                    oldReport.image_id === report.card_id
            );

            if (exists) {
                return oldReports;
            }

            const newReport: Report = {
                image_id: report.image_id,
                image_path: report.image_path,
                latitude: report.latitude,
                longitude: report.longitude,
                status: report.status,
                description: report.description,
                user_id: report.user_id
            };

            return [
                newReport,
                ...oldReports
            ];
        });
    }


    function handleRemoveReport(reportId: number): void {

        setReports((oldReports) =>
            oldReports.filter(
                (oldReport) =>
                    oldReport.image_id !== reportId
            )
        );
    }


    function handleStatusUpdate(
        data: StatusUpdate
    ): void {

        setReports((oldReports) =>
            oldReports.map(
                (report) =>
                    report.image_id === data.card_id
                        ? {
                            ...report,
                            status: data.status
                        }
                        : report
            )
        );
    }


    function handleDescriptionUpdate(
        data: DescriptionUpdate
    ): void {

        setReports((oldReports) =>
            oldReports.map(
                (report) =>
                    report.image_id === data.card_id
                        ? {
                            ...report,
                            description: data.description
                        }
                        : report
            )
        );
    }


    useEffect(() => {
        console.log("🟢 Grid listener setup");

        // socket.on(
        //     "new_report",
        //     handleNewReport
        // );
        // console.log("🟢 Listend");

        socket.on("new_report", (report) => {
        console.log("🟢 NEW REPORT RECEIVED:", report);

        handleNewReport(report);
        });


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

        return () => {

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
                "update_description",
                handleDescriptionUpdate
            );

        };

    }, []);


    return (

        <div
            className="cards-grid"
            id="disaster-feed"
        >

            {reports.map((report) => {

                const userActions =
                    userActionMap[report.image_id];

                const canDelete =
                    report.user_id=== currentUserId;

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