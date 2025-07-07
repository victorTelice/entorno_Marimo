# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "fastapi==0.115.12",
#     "marimo",
#     "mohtml==0.1.10",
#     "requests==2.32.3",
#     "uvicorn==0.34.3",
# ]
# ///

import marimo

__generated_with = "0.14.9"
app = marimo.App(width="columns")


@app.cell(column=0, hide_code=True)
def _(mo):
    mo.md(r"""## Server Setup""")
    return


@app.cell
def _():
    import marimo as mo
    import threading
    import asyncio
    import time
    import uvicorn
    return asyncio, mo, threading, time, uvicorn


@app.cell
def _(mo):
    get_server_thread, set_server_thread = mo.state(None)
    get_current_server, set_current_server = mo.state(None)
    return (
        get_current_server,
        get_server_thread,
        set_current_server,
        set_server_thread,
    )


@app.cell
def _(uvicorn):
    class StoppableServer:
        def __init__(self, app, host="0.0.0.0", port=8000):
            self.config = uvicorn.Config(app, host=host, port=port)
            self.server = uvicorn.Server(self.config)

        async def serve(self):
            await self.server.serve()

        def stop(self):
            if self.server:
                self.server.should_exit = True
                # Also force close any existing servers
                if hasattr(self.server, "servers"):
                    for server in self.server.servers:
                        server.close()
    return (StoppableServer,)


@app.cell
def _():
    return


@app.cell(column=1, hide_code=True)
def _(mo):
    mo.md(r"""## Developer Experience live updates!""")
    return


@app.cell
def _(FastAPI, HTMLResponse, JSONResponse, div, p):
    app = FastAPI()


    @app.get("/", response_class=HTMLResponse)
    def read_root():
        return str(div(p("hello", klass="text-2xl text-center text-blue-500")))


    @app.get("/api", response_class=JSONResponse)
    def read_root():
        return {"alive": "yes!!"}
    return (app,)


@app.cell
def _(PORT, div, rq):
    div(rq.get(f"http://localhost:{PORT}/").text)
    return


@app.cell
def _(PORT, rq):
    rq.get(f"http://localhost:{PORT}/api").json()
    return


@app.cell
def _():
    from mohtml import div, p, head, body, tailwind_css, html
    from fastapi import FastAPI, Response
    from fastapi.responses import HTMLResponse, JSONResponse

    tailwind_css()
    return FastAPI, HTMLResponse, JSONResponse, div, p


@app.cell
def _(get_server_thread):
    import requests as rq

    get_server_thread()
    return (rq,)


@app.cell
def _():
    PORT = 12345
    return (PORT,)


@app.cell
def _(
    PORT,
    StoppableServer,
    app,
    asyncio,
    get_current_server,
    get_server_thread,
    mo,
    set_current_server,
    set_server_thread,
    threading,
    time,
):
    # Estados
    status, set_status = mo.state("detenido")
    logs, set_logs = mo.state([])

    def log(msg):
        timestamp = time.strftime("%H:%M:%S")
        set_logs(logs() + [f"[{timestamp}] {msg}"])

    def start_server():
        if get_server_thread() and get_server_thread().is_alive():
            log("Servidor ya está corriendo")
            set_status("activo")

        set_current_server(StoppableServer(app, host="0.0.0.0", port=PORT))

        def run():
            asyncio.run(get_current_server().serve())

        t = threading.Thread(target=run, daemon=True)
        t.start()
        set_server_thread(t)
        log(f"Servidor iniciado en el puerto {PORT}")
        set_status("activo")

    def stop_server():
        if get_server_thread() and get_server_thread().is_alive():
            get_current_server().stop()
            get_server_thread().join(timeout=2)
            set_server_thread(None)
            set_current_server(None)
            log("Servidor detenido manualmente")
            set_status("detenido")
        else:
            log("No hay servidor activo")
            set_status("detenido")

    estado = mo.md(
        f"""**Estado:** {"🟢 Activo" if status() == "activo" else "🔴 Detenido"}"""
    )

    log_markdown = "\n".join(f"- {line}" for line in logs()[-20:])  # Últimos 20 logs

    mo.vstack([
        mo.hstack([
            mo.ui.button(label="🚀 Iniciar Servidor", on_click=start_server),
            mo.ui.button(label="🛑 Detener Servidor", on_click=stop_server),
            estado
        ]),
        mo.md("### Logs del servidor"),
        mo.md(log_markdown)
    ])
    return


@app.cell(column=2)
def _():
    return


if __name__ == "__main__":
    app.run()
