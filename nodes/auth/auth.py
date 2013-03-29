import json

from urllib import urlencode

from twisted.web import http
from twisted.web.server import NOT_DONE_YET
from twisted.web.client import getPage

from warp.common.avatar import Avatar
from warp.runtime import avatar_store, config

def uni(st, coding="utf-8"):
    if isinstance(st, unicode):
        return st
    return unicode(st, coding)

def get(request, name, default = None):
    return request.args.get(name, [default])[0]

def JSON(handler):
    def wrapped(request):
        data = handler(request)
        return json.dumps(data)
    return wrapped

def ok(result, request):
    # store = request.store
    data = json.loads(result)

    print >>config["log"], "Result ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print >>config["log"], result
    if data.get("status") == "okay":
        email = uni(data.get("email"))

        # raise Exception("In progress")

        avatar = avatar_store.find(Avatar, email = email).one()
        if not avatar:
            avatar = Avatar()
            avatar.email = email
            avatar_store.add(avatar)
            avatar_store.commit()
        request.session.setAvatarID(avatar.id)
        request.avatar = request.session.avatar

        return {
            "success": True,
            "data": data
        }
        # request.write(json.dumps({
        #     "success": True,
        #     "data": data
        # }))
        # request.finish()
    else:
        raise Exception("Login failed")

def error(failure, request):
    print >>config["log"], "Error ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print >>config["log"], failure
    # request.write(json.dumps({
    #     "success": False,
    #     "error": failure
    # }))
    # request.finish()
    # print >>config["log"], "Error done"
    return {
        "success": False,
        "error": failure
    }

def done(final, request):
    print >>config["log"], "Done ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print >>config["log"], final
    raw = json.dumps(final)
    request.setResponseCode(http.OK)
    request.setHeader("content-type", "application/json")
    request.setHeader("content-length", str(len(raw)))
    request.write(raw)
    request.finish()

def render_login(request):
    assertion = get(request, "assertion")
    assert assertion

    data = {
        "assertion": assertion,
        # FIX
        "audience": "http://%s" % config["domain"]
    }
    headers = {
        "Content-Type": "application/json"
    }

    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    # print data

    d = getPage("https://verifier.login.persona.org/verify", method = "POST",
                headers = headers, postdata = json.dumps(data))
    d.addCallback(ok, request)
    d.addErrback(error, request)
    d.addBoth(done, request)

    print "Requesting"

    return NOT_DONE_YET

@JSON
def render_logout(request):
    request.session.setAvatarID(None)
    return {"success": True}
