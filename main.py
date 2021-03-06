# standard imports
from flask import Flask, request, render_template, session, redirect, url_for
from env import secret_key
from database import SqlOperations
from validation import Validation
from config import Config

# variable configurations
app = Flask(__name__)
app.secret_key = secret_key
config = Config()
sql = SqlOperations(config)
val = Validation(config)


@app.route("/")
def root():
    for key in list(session.keys()):
        session.pop(key)
    return render_template("index.html")


@app.route("/routes", methods=["POST", "GET"])
def routes():
    """
    /routes handles input to search for bus services between two bus stops, output the result and redirects 
    to /list_stops
    """
    # list of error messages
    err_msgs = [None]*5
    # list of headers to be displayed
    headers = ["Bus No.", "Distance (in km)", "Fare (in cents)"]
    # list of descriptions of all bus stops
    descs = sql.get_all_bus_stops()
    if request.method == "GET":
        if request.args.get("_", None) is None:
            # render input page
            return render_template("input.html", descs=descs, err_msgs=err_msgs)
        elif request.args.get("_", None) != '':
            return redirect(url_for("routes"))
        else:
            # render previous search results
            results = session.get("results", None)
            entry = session.get("entry", None)
            if entry is None or results is None:
                return redirect(url_for("routes"))
            return render_template("routes.html", results=results, headers=headers, entry=entry)
    else:
        # retrieve form submission
        entry = {key: request.form.get(key, None) for key in ["start", "end", "mode", "group", "payment_mode"]}
        val.set_params(entry)
        # retrieve validation results
        err_msgs, passed = val.check_all_input()
        if not passed:
            # render input page if input validation fails
            return render_template("input.html", descs=descs, err_msgs=err_msgs)
        # find bus routes through both bus stops
        bus_routes, b1_code, b2_code = sql.find_routes(entry["start"], entry["end"])
        # check if such bus routes exist
        err_msgs, passed = val.check_routes(bus_routes, entry["start"], entry["end"], err_msgs)
        if not passed:
            # render input page if routes verification fails, error message will be displayed
            return render_template("input.html", descs=descs, err_msgs=err_msgs)
        # retrieve entries for table
        results = sql.optimal(entry["mode"], b1_code, b2_code, bus_routes, entry["group"], entry["payment_mode"])
        # additional description to label
        if entry["group"] in ["student", "senior", "workfare"]:
            entry["group"] += " concession pass"
        # store previous search results in the session
        session["route_direction"] = {x[0]: x[1] for x in bus_routes}
        session["results"], session["entry"] = results, entry
        return render_template("routes.html", results=results, headers=headers, entry=entry)


@app.route("/list_stops", methods=["GET", "POST"])
def list_stops():
    """
    /list_stops displays the all stops on a specific bus route. 
    It can redirect the user back to /routes  
    """
    if request.method == "GET":
        if session.get("route_direction", None) is None:
            # redirects user back to search page if no routes were recorded
            return redirect(url_for("routes"))
        route = request.args.get("route", None)
        # retrieves direction of the route desired
        direction = session["route_direction"].get(route, None)
        if direction is None:
            # redirects user back to search page if no routes were recorded or the route to search is invalid
            return redirect(url_for("routes"))
        # queries search results
        results = sql.get_all_stops(route, direction)
        return render_template("stops.html", route=route, results=results)
    else:
        return redirect(url_for("routes"))

app.run('0.0.0.0')
