from flask import Flask, render_template
from routes.url_routes import url_bp
from routes.stats_routes import stats_bp
from middleware.rate_limiter import check_rate_limit


def create_app():
    app = Flask(__name__)

    @app.before_request
    def rate_limit():
        result = check_rate_limit()

        if result:
            return result

    app.register_blueprint(url_bp)
    app.register_blueprint(stats_bp)

    @app.route("/")
    def home():
        return render_template("index.html")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
