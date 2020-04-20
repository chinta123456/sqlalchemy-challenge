import datetime as dt

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


# Database Setup #
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement).all()
    prec_list = []
    for date in results:
        prec_dict = {}
        prec_dict[f"{date.date}"] = date.prcp
        prec_list.append(prec_dict)
        
    return jsonify(prec_list)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    station_list = list(np.ravel(results))
        
    return jsonify(station_list)
    
@app.route("/api/v1.0/tobs")
def tobs():
    # Calculate the date 1 year ago from the last data point in the database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).\
        order_by(Measurement.date.desc()).all()
    
    data_list = list(np.ravel(data))
    
    return jsonify(data_list)
 
@app.route("/api/v1.0/<start>")
def start(start):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    calc_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    
    data_list = list(np.ravel(calc_data))
    
    return jsonify(data_list)

@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    calc_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    data_list = list(np.ravel(calc_data))
    
    return jsonify(data_list)



if __name__ == '__main__':
    app.run(debug=True)