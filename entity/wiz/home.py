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
            <h1 style="text-align: center; color: red; font-size: 72px;">CS 4501</h1>
            <p>Group 3: Andrew Ton, Brandon Peck, Michelle Wang</p>
    </body>
</html>
"""
	return HttpResponse(httpcode)

    