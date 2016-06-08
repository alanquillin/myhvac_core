from myhvac_core.db import api as db
from myhvac_core.db import models

from datetime import datetime, timedelta


def get_current_temp():
    def do(session):
        temp_agg = 0
        temp_cnt = 0

        room_models = db.get_rooms_dashboard(session)

        for room_model in room_models:
            if not room_model.active:
                continue

            room_temp = None
            measurement_agg = 0
            measurement_cnt = 0

            if room_model.sensors:
                for sensor_model in room_model.sensors:
                    measurement = db.get_most_recent_sensor_temperature(session,
                                                                        sensor_id=sensor_model.id,
                                                                        order_desc=True,
                                                                        order_by=models.Measurement.recorded_date)

                    if measurement and measurement.recorded_date > datetime.now() - timedelta(minutes=12):
                        measurement_agg = measurement.measurement
                        measurement_cnt = measurement_cnt + 1

            if measurement_cnt > 0 and measurement_agg > 0:
                room_temp = measurement_agg / measurement_cnt

            if room_temp:
                temp_agg = temp_agg + (room_temp * room_model.weight)
                temp_cnt = temp_cnt + room_model.weight

        if not temp_cnt and not temp_agg:
            raise Exception('No current temperature data found...')

        return temp_agg / temp_cnt

    return db.sessionize(do)
