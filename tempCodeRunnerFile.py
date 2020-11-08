ect")
        session['user_id'] = user[0].id
        session["user_name"] = user[0].name
        return redirect("/search" )
    else :