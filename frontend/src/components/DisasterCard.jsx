import CardActions from "./CardActions.jsx";
import '../style/DisasterCard.css'

function DisasterCard({ report, user_actions, canDelete }) {

    const imageHTML = report.image_path ? (

        <img
            src={report.image_path}
            className="cimg"
            alt="Disaster photo"
        />

    ) : (

        <div className="cimg-placeholder">
            <i className="ti ti-photo"></i>
        </div>

    );


    return (

        <div className="dcard">

            <div className="cimg-slot">
                {imageHTML}
            </div>


            <div className="cbody">

                <span className={`ctag ${report.status}`}>
                    {report.status}
                </span>


                <p className="ccap">
                    {report.description}
                </p>


                <CardActions
                    report={report}
                    user_actions={user_actions}
                    canDelete={canDelete}
                />

            </div>

        </div>

    );
}

export default DisasterCard;