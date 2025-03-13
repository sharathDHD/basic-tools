# file_path/dashboard.py
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import base64
import hashlib
import io
from dash.dependencies import Input, Output, State
from PIL import Image

# Initialize Dash app with a light Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Override the default index_string to include  CSS styles.
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title> Dashboard</title>
        {%favicon%}
        {%css%}
        <style>
            /* styling */
            body {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                background-color: #F0F0F5;
                color: #333;
                margin: 0;
                padding: 0;
            }
            .card {
                border: none;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                margin-bottom: 1.5rem;
            }
            .card-body {
                padding: 1.5rem;
            }
            .btn {
                border-radius: 5px;
                padding: 0.5rem 1rem;
                font-weight: 600;
            }
            .modal-content {
                border-radius: 8px;
            }
            h1 {
                font-weight: 600;
                margin-bottom: 2rem;
            }
            .container {
                padding-top: 2rem;
                padding-bottom: 2rem;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Utility Functions
def base64_to_image_obj(base64_string):
    try:
        image_data = base64.b64decode(base64_string)
        image = Image.open(io.BytesIO(image_data))
        return image
    except Exception:
        return None

def image_to_base64_str(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def get_md5(text):
    return hashlib.md5(text.encode()).hexdigest()

def check_base64_type(base64_string):
    try:
        decoded_data = base64.b64decode(base64_string)
        # Check for JPEG signature
        if decoded_data.startswith(b"\xFF\xD8\xFF"):
            return "Image (JPEG)"
        # Check for PNG signature
        elif decoded_data.startswith(b"\x89PNG\r\n\x1a\n"):
            return "Image (PNG)"
        else:
            try:
                decoded_data.decode("utf-8")
                return "Text"
            except UnicodeDecodeError:
                return "Unknown"
    except Exception:
        return "Invalid Base64"

def text_to_sha1_sha256(text):
    sha1_hash = hashlib.sha1(text.encode()).hexdigest()
    sha256_hash = hashlib.sha256(text.encode()).hexdigest()
    return sha1_hash, sha256_hash

def image_to_sha1_sha256(image_data):
    sha1_hash = hashlib.sha1(image_data).hexdigest()
    sha256_hash = hashlib.sha256(image_data).hexdigest()
    return sha1_hash, sha256_hash

# Layout with 9 expandable cards
app.layout = dbc.Container([
    html.H1(" Dashboard", className="text-center"),
    
    dbc.Row([
        dbc.Col(dbc.Card([dbc.CardBody([html.H5("Base64 to Image"), 
                                          dbc.Button("Expand", id="open-modal-1", color="primary")])]), width=4),
        dbc.Col(dbc.Card([dbc.CardBody([html.H5("Image to Base64"), 
                                          dbc.Button("Expand", id="open-modal-2", color="success")])]), width=4),
        dbc.Col(dbc.Card([dbc.CardBody([html.H5("MD5 Checksum"), 
                                          dbc.Button("Expand", id="open-modal-3", color="danger")])]), width=4),
    ], className="mt-4"),

    dbc.Row([
        dbc.Col(dbc.Card([dbc.CardBody([html.H5("Text to MD5"), 
                                          dbc.Button("Expand", id="open-modal-4", color="info")])]), width=4),
        dbc.Col(dbc.Card([dbc.CardBody([html.H5("Valid MD5 to Text"), 
                                          dbc.Button("Expand", id="open-modal-5", color="warning")])]), width=4),
        dbc.Col(dbc.Card([dbc.CardBody([html.H5("Compare MD5 Hashes"), 
                                          dbc.Button("Expand", id="open-modal-6", color="secondary")])]), width=4),
    ], className="mt-4"),
    
    dbc.Row([
        dbc.Col(dbc.Card([dbc.CardBody([html.H5("Check Base64 Type"), 
                                          dbc.Button("Expand", id="open-modal-7", color="dark")])]), width=4),
        dbc.Col(dbc.Card([dbc.CardBody([html.H5("Text to SHA-1 & SHA-256"), 
                                          dbc.Button("Expand", id="open-modal-8", color="primary")])]), width=4),
        dbc.Col(dbc.Card([dbc.CardBody([html.H5("Image to SHA-1 & SHA-256"), 
                                          dbc.Button("Expand", id="open-modal-9", color="success")])]), width=4),
    ], className="mt-4"),

    # Modals for each functionality
    dbc.Modal([
        dbc.ModalHeader("Base64 to Image Converter"),
        dbc.ModalBody([
            dcc.Textarea(id="base64-input", placeholder="Enter Base64 string...", style={"width": "100%", "height": "100px"}),
            html.Br(), html.Br(),
            dbc.Button("Convert", id="convert-base64-btn", color="primary"),
            html.Br(), html.Br(),
            html.Img(id="decoded-image", style={"max-width": "100%"})
        ]),
        dbc.ModalFooter(dbc.Button("Close", id="close-modal-1", className="ml-auto")),
    ], id="modal-1", is_open=False),

    dbc.Modal([
        dbc.ModalHeader("Image to Base64 Converter"),
        dbc.ModalBody([
            dcc.Upload(id="upload-image-to-base64", children=html.Button("Upload Image"), multiple=False),
            html.Br(), html.Br(),
            html.Div(id="base64-output", style={"word-wrap": "break-word", "max-height": "300px", "overflow": "auto"}),
        ]),
        dbc.ModalFooter(dbc.Button("Close", id="close-modal-2", className="ml-auto")),
    ], id="modal-2", is_open=False),

    dbc.Modal([
        dbc.ModalHeader("MD5 Checksum Generator"),
        dbc.ModalBody([
            dcc.Upload(id="upload-file-md5", children=html.Button("Upload File"), multiple=False),
            html.Br(), html.Br(),
            html.Div(id="md5-output"),
        ]),
        dbc.ModalFooter(dbc.Button("Close", id="close-modal-3", className="ml-auto")),
    ], id="modal-3", is_open=False),

    dbc.Modal([
        dbc.ModalHeader("Text to MD5 Converter"),
        dbc.ModalBody([
            dcc.Input(id="text-md5-input", type="text", placeholder="Enter text...", style={"width": "100%"}),
            html.Br(), html.Br(),
            html.Div(id="text-md5-output"),
        ]),
        dbc.ModalFooter(dbc.Button("Close", id="close-modal-4", className="ml-auto")),
    ], id="modal-4", is_open=False),

    dbc.Modal([
        dbc.ModalHeader("Valid MD5 to Text"),
        dbc.ModalBody([
            dcc.Input(id="md5-to-text-input", type="text", placeholder="Enter MD5 hash...", style={"width": "100%"}),
            html.Br(), html.Br(),
            html.Div(id="md5-to-text-output"),
        ]),
        dbc.ModalFooter(dbc.Button("Close", id="close-modal-5", className="ml-auto")),
    ], id="modal-5", is_open=False),

    dbc.Modal([
        dbc.ModalHeader("Compare Two MD5 Hashes"),
        dbc.ModalBody([
            dcc.Input(id="md5-compare-1", type="text", placeholder="Enter first MD5 hash...", style={"width": "100%"}),
            dcc.Input(id="md5-compare-2", type="text", placeholder="Enter second MD5 hash...", style={"width": "100%", "marginTop": "10px"}),
            html.Br(), html.Br(),
            html.Div(id="md5-compare-output"),
        ]),
        dbc.ModalFooter(dbc.Button("Close", id="close-modal-6", className="ml-auto")),
    ], id="modal-6", is_open=False),

    dbc.Modal([
        dbc.ModalHeader("Check Base64 Type"),
        dbc.ModalBody([
            dcc.Textarea(id="base64-check-input", placeholder="Enter Base64 string...", style={"width": "100%", "height": "100px"}),
            html.Br(), html.Br(),
            dbc.Button("Check", id="check-base64-btn", color="primary"),
            html.Br(), html.Br(),
            html.Div(id="base64-check-output"),
        ]),
        dbc.ModalFooter(dbc.Button("Close", id="close-modal-7", className="ml-auto")),
    ], id="modal-7", is_open=False),

    dbc.Modal([
        dbc.ModalHeader("Text to SHA-1 & SHA-256"),
        dbc.ModalBody([
            dcc.Textarea(id="text-sha-input", placeholder="Enter text...", style={"width": "100%", "height": "100px"}),
            html.Br(), html.Br(),
            dbc.Button("Generate", id="text-sha-btn", color="primary"),
            html.Br(), html.Br(),
            html.Div(id="text-sha-output"),
        ]),
        dbc.ModalFooter(dbc.Button("Close", id="close-modal-8", className="ml-auto")),
    ], id="modal-8", is_open=False),

    dbc.Modal([
        dbc.ModalHeader("Image to SHA-1 & SHA-256"),
        dbc.ModalBody([
            dcc.Upload(id="upload-image-sha", children=html.Button("Upload Image"), multiple=False),
            html.Br(), html.Br(),
            html.Div(id="image-sha-output"),
        ]),
        dbc.ModalFooter(dbc.Button("Close", id="close-modal-9", className="ml-auto")),
    ], id="modal-9", is_open=False),
], fluid=True)

# Callbacks for toggling modals
for i in range(1, 10):
    @app.callback(
        Output(f"modal-{i}", "is_open"),
        [Input(f"open-modal-{i}", "n_clicks"), Input(f"close-modal-{i}", "n_clicks")],
        [State(f"modal-{i}", "is_open")]
    )
    def toggle_modal(open_click, close_click, is_open):
        if open_click or close_click:
            return not is_open
        return is_open

# Callback for Base64 to Image conversion
@app.callback(
    Output("decoded-image", "src"),
    Input("convert-base64-btn", "n_clicks"),
    State("base64-input", "value")
)
def convert_base64(n_clicks, base64_string):
    if n_clicks and base64_string:
        try:
            # Decode and then re-encode to ensure proper formatting for display
            image_data = base64.b64decode(base64_string)
            return "data:image/png;base64," + base64.b64encode(image_data).decode('utf-8')
        except Exception:
            return None
    return None

# Callback for Image to Base64 conversion
@app.callback(
    Output("base64-output", "children"),
    Input("upload-image-to-base64", "contents")
)
def upload_to_base64(contents):
    if contents:
        return contents.split(",")[1]
    return ""

# Callback for MD5 checksum calculation (File Upload)
@app.callback(
    Output("md5-output", "children"),
    Input("upload-file-md5", "contents")
)
def compute_md5_callback(contents):
    if contents:
        _, content_string = contents.split(',')
        file_bytes = base64.b64decode(content_string)
        return f"MD5: {hashlib.md5(file_bytes).hexdigest()}"
    return ""

# Callback for Text to MD5 conversion
@app.callback(
    Output("text-md5-output", "children"),
    Input("text-md5-input", "value")
)
def text_to_md5(value):
    return hashlib.md5(value.encode()).hexdigest() if value else ""

# For demonstration, using a simple dictionary for Valid MD5 to Text.
md5_text_db = {
    hashlib.md5("hello".encode()).hexdigest(): "hello",
    hashlib.md5("world".encode()).hexdigest(): "world",
}
@app.callback(
    Output("md5-to-text-output", "children"),
    Input("md5-to-text-input", "value")
)
def md5_to_text(value):
    return md5_text_db.get(value, "Unknown hash") if value else ""

# Callback for Compare MD5 Hashes
@app.callback(
    Output("md5-compare-output", "children"),
    [Input("md5-compare-1", "value"), Input("md5-compare-2", "value")]
)
def compare_md5(v1, v2):
    if v1 and v2:
        return "Match" if v1 == v2 else "Different"
    return ""

# Callback for Check Base64 Type
@app.callback(
    Output("base64-check-output", "children"),
    Input("check-base64-btn", "n_clicks"),
    State("base64-check-input", "value")
)
def check_base64(n_clicks, base64_string):
    if n_clicks and base64_string:
        return check_base64_type(base64_string)
    return ""

# Callback for Text to SHA-1 & SHA-256 conversion
@app.callback(
    Output("text-sha-output", "children"),
    Input("text-sha-btn", "n_clicks"),
    State("text-sha-input", "value")
)
def generate_text_sha(n_clicks, text):
    if n_clicks and text:
        sha1_hash, sha256_hash = text_to_sha1_sha256(text)
        return f"SHA-1: {sha1_hash}\nSHA-256: {sha256_hash}"
    return ""

# Callback for Image to SHA-1 & SHA-256 conversion
@app.callback(
    Output("image-sha-output", "children"),
    Input("upload-image-sha", "contents")
)
def generate_image_sha(contents):
    if contents:
        _, content_string = contents.split(',')
        image_data = base64.b64decode(content_string)
        sha1_hash, sha256_hash = image_to_sha1_sha256(image_data)
        return f"SHA-1: {sha1_hash}\nSHA-256: {sha256_hash}"
    return ""

if __name__ == "__main__":
    app.run_server(debug=True)
