from flask import request, redirect, url_for, render_template, session, flash
from flask_restful import Resource
from api_views import room_list, user_list
from dataclasses import asdict

from data.dict2obj import dict2User
from data.models import Chatroom as Room

# Shows a single room
from validation.input_validations import room_name_validation, select_validation


class SingleRoom(Resource):

    def get(self, room_id: str = None):
        for room in room_list:
            if room.room_id == room_id:
                return asdict(room)
        return {"message": "Room not found"}, 404

    # Deletes a room
    def post(self, room_id: str = None):
        for room in room_list:
            if room.room_id == room_id:
                room_list.remove(room)
                flash(message=f"Room '{room.name}' has been deleted", category="success")
                return redirect(url_for('get_home'))
        return {"message": "Room not found"}, 404


# Shows a list of rooms
class RoomList(Resource):

    def get(self):
        return [asdict(room) for room in room_list]

    def post(self):
        if request.method == 'POST':
            room_name = request.form['room_name']
            room_type = request.form['room_type']
            name_failed = room_name_validation(room_name)
            room_type_failed = select_validation(room_type)
            if name_failed or room_type_failed:
                if name_failed:
                    flash(message=name_failed, category="danger")
                if room_type_failed:
                    flash(message=room_type_failed, category="danger")
                return redirect(url_for('get_home'))
            bot_user = get_bot(room_type)
            current_user = session['user']
            current_user = dict2User(current_user)
            room = Room(name=room_name, creator=current_user, users=[bot_user, current_user])
            room_list.append(room)
            flash(message=f"Room '{room.name}' has been successfully created!", category="success")
            return redirect(url_for('get_home'))

        flash(message="Cannot create room, please try again!", category="warning")
        return render_template('home.html')


def get_bot(room_type):
    return [user for user in user_list if user.personality == room_type][0]
