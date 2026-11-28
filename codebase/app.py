"""Bản chạy thử: `python run.py` mở giao diện web (codebase/web.py) và mở trình duyệt.

- Mặc định: web — cùng answer() trong agent.py, cùng input như bộ câu thử.
- `NO_BROWSER=1` để không tự mở trình duyệt. `python codebase/app.py --cli`: khung dòng lệnh cũ — gõ đầu vào → answer() → in kết quả.
Không sửa run.py (khung); run.py gọi file này.
"""
import os
import sys

for _stream in (sys.stdout, sys.stderr, sys.stdin):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def _where(e):
    """File (trong codebase/) gây lỗi khi nạp: SyntaxError có e.filename, lỗi khác lấy khung cuối của traceback."""
    import traceback
    path = getattr(e, "filename", None) or (traceback.extract_tb(e.__traceback__)[-1].filename if e.__traceback__ else "")
    if not path:
        return "codebase/"
    p = os.path.abspath(path)
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.relpath(p, base).replace(os.sep, "/") if p.startswith(base) else path

def web() -> int:
    try:
        import web as web_ui
    except Exception as e:
        print("Không nạp được codebase/ — lỗi ở %s: %s: %s" % (_where(e), type(e).__name__, e))
        return 1
    if not web_ui.ON_HOST and not os.environ.get("NO_BROWSER"):
        import threading
        import webbrowser
        threading.Timer(1.0, webbrowser.open, ["http://127.0.0.1:%d" % web_ui.PORT]).start()
    return web_ui.main()


def main() -> int:
    if "--cli" not in sys.argv:
        return web()
    try:
        import tracing
        from agent import answer
    except Exception as e:  # lỗi cú pháp, thiếu thư viện… trong codebase/
        print("Không nạp được codebase/ — lỗi ở %s: %s: %s" % (_where(e), type(e).__name__, e))
        print("Sửa lỗi rồi chạy lại. Cách nối model: docs/connect-model.md")
        return 1
    print("Bản chạy thử — gõ đầu vào rồi Enter. Thoát: Ctrl+C (hoặc Enter 2 lần với dòng trống).")
    blank = 0
    while True:
        try:
            text = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not text:
            blank += 1
            if blank >= 2:
                return 0
            continue
        blank = 0
        tracing.begin("app")
        try:
            result = answer(text)
        except NotImplementedError as e:
            tracing.end()
            print("Chưa nối model: %s" % e)
            return 1
        except Exception as e:  # lỗi gọi model: báo rồi cho hỏi tiếp
            tracing.end()
            print("[lỗi] %s: %s" % (type(e).__name__, e))
            continue
        s, _ = tracing.end()
        print(result.get("output", "") if isinstance(result, dict) else result)
        print("   (model: %s · gọi model %d lần · công cụ %d lần · token vào %d / ra %d)"
              % (", ".join(s["models"]) or "—", s["model_calls"], s["tool_calls"], s["tokens_in"], s["tokens_out"]))


if __name__ == "__main__":
    sys.exit(main())
