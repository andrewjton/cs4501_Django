from django.http import HttpResponse

def index(request):
	httpcode = """
<!DOCTYPE HTML>
<html>
    <head>
        <meta charset="UTF-8">
        <title>1st Django Project</title>
    </head>
    <body>
            <h1 style="text-align: center; color: red; font-size: 72px;">Hello World!</h1>
            <img src="http://andrewton.net/content/profPic.png" alt="andrew ton. for blind people">
    </body>
</html>
"""
	return HttpResponse(httpcode)

    