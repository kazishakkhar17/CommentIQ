# File: app.py

import gradio as gr
from src.agent import CommentAnalysisAgent
from src.response_generator import ResponseGenerator
import pandas as pd
import json
import time
from datetime import datetime

# =============================================================================
# SHARED STATE
# =============================================================================

inbox = []
history = []

def get_time():
    return datetime.now().strftime("%H:%M")

# =============================================================================
# INITIALIZE
# =============================================================================

print("Initializing CommentIQ...")
agent = CommentAnalysisAgent()
generator = ResponseGenerator()
print("✅ CommentIQ ready")

# =============================================================================
# CORE LOGIC
# =============================================================================

def process_comment(comment, language):
    if not comment.strip():
        return None, None
    analysis = agent.analyze(comment, user_id="demo_user", use_rag=False)
    emotion  = analysis['final_prediction']['emotion']
    response = generator.generate(emotion, language)
    return analysis, response

# =============================================================================
# TAB 1 — USER PANEL
# =============================================================================

def user_post_comment(comment, language, chat_history):
    if not comment.strip():
        return chat_history, "", "Please enter a comment."

    analysis, response = process_comment(comment, language)
    emotion  = analysis['final_prediction']['emotion']
    decision = analysis['final_prediction']['decision']
    msg_id   = f"msg_{int(time.time()*1000)}"
    ts       = get_time()

    chat_history = chat_history or []
    chat_history.append({"role": "user", "content": comment})

    if decision == 'NO_REPLY':
        history.append({
            'id': msg_id, 'user_text': comment, 'reply': None,
            'emotion': emotion, 'decision': 'NO_REPLY',
            'time': ts, 'analysis': analysis
        })
        return chat_history, "", "🚫 Comment flagged as spam. No reply sent."

    elif decision == 'AUTO_REPLY':
        reply_text = response['response_text']
        chat_history.append({"role": "assistant", "content": reply_text})
        history.append({
            'id': msg_id, 'user_text': comment, 'reply': reply_text,
            'emotion': emotion, 'decision': 'AUTO_REPLY',
            'time': ts, 'analysis': analysis
        })
        return chat_history, "", f"✅ Auto-replied ({emotion})"

    else:
        chat_history.append({
            "role": "assistant",
            "content": "_(Our team will respond shortly...)_"
        })
        inbox.append({
            'id': msg_id, 'user_text': comment, 'reply': None,
            'emotion': emotion, 'decision': decision,
            'time': ts, 'analysis': analysis,
            'chat_idx': len(chat_history) - 1
        })
        return chat_history, "", f"⏳ Sent to admin inbox ({emotion}, {analysis['final_prediction']['confidence']:.0%} confidence)"

# =============================================================================
# TAB 2 — ADMIN INBOX
# =============================================================================

def get_inbox_df():
    pending = [m for m in inbox if m['reply'] is None]
    if not pending:
        return pd.DataFrame(columns=['#', 'Time', 'Emotion', 'Confidence', 'Decision', 'Comment'])
    rows = []
    for i, m in enumerate(pending):
        a = m['analysis']
        rows.append({
            '#':          i,
            'Time':       m['time'],
            'Emotion':    m['emotion'],
            'Confidence': f"{a['final_prediction']['confidence']:.0%}",
            'Decision':   m['decision'],
            'Comment':    m['user_text'][:80] + ('...' if len(m['user_text']) > 80 else '')
        })
    return pd.DataFrame(rows)

def load_inbox_message(evt: gr.SelectData):
    pending = [m for m in inbox if m['reply'] is None]
    if not pending or evt.index[0] >= len(pending):
        return "", "", "", "", ""

    m  = pending[evt.index[0]]
    a  = m['analysis']
    bp = a['base_prediction']
    fp = a['final_prediction']

    tools_str = ", ".join(a['tools_used']) if a['tools_used'] else "None"
    adj_str   = "\n".join(
        f"  • {x['tool']}: {x.get('change', x.get('insight', x.get('reason', '')))}"
        for x in a['adjustments_made']
    ) if a['adjustments_made'] else "  None"

    analysis_text = (
        f"Comment:     {m['user_text']}\n"
        f"Time:        {m['time']}\n\n"
        f"Base model:  {bp['emotion']} ({bp['confidence']:.0%})\n"
        f"Final:       {fp['emotion']} ({fp['confidence']:.0%})\n"
        f"Decision:    {fp['decision']}\n\n"
        f"Tools used:  {tools_str}\n"
        f"Adjustments:\n{adj_str}"
    )

    suggested = generator.generate(fp['emotion'], 'bengali')['response_text'] or ""

    return (
        m['id'],
        m['user_text'],
        analysis_text,
        suggested,
        f"{fp['emotion']} · {fp['confidence']:.0%} confidence · {fp['decision']}"
    )

def send_admin_reply(msg_id, reply_text, chat_history):
    if not msg_id or not reply_text.strip():
        return chat_history, get_inbox_df(), "Please select a message and write a reply."

    msg = next((m for m in inbox if m['id'] == msg_id), None)
    if not msg:
        return chat_history, get_inbox_df(), "Message not found."

    msg['reply'] = reply_text
    chat_history = chat_history or []

    idx = msg.get('chat_idx', -1)
    if 0 <= idx < len(chat_history):
        chat_history[idx] = {"role": "assistant", "content": reply_text}

    history.append({
        'id':        msg['id'],
        'user_text': msg['user_text'],
        'reply':     reply_text,
        'emotion':   msg['emotion'],
        'decision':  'HUMAN_REVIEW',
        'time':      msg['time'],
        'analysis':  msg['analysis']
    })

    return chat_history, get_inbox_df(), "✅ Reply sent"

# =============================================================================
# TAB 3 — HISTORY
# =============================================================================

def get_history_df():
    if not history:
        return pd.DataFrame(columns=['Time', 'Emotion', 'Decision', 'Comment', 'Reply'])
    rows = []
    for m in reversed(history):
        rows.append({
            'Time':     m['time'],
            'Emotion':  m['emotion'],
            'Decision': m['decision'],
            'Comment':  m['user_text'][:60] + ('...' if len(m['user_text']) > 60 else ''),
            'Reply':    (m['reply'] or 'No reply')[:60]
        })
    return pd.DataFrame(rows)

def refresh_history():
    return get_history_df()

# =============================================================================
# TAB 4 — BATCH ANALYSIS
# =============================================================================

def batch_analysis(file):
    if file is None:
        return pd.DataFrame()
    df = pd.read_csv(file.name)
    if 'comment_text' not in df.columns:
        return pd.DataFrame({'Error': ['CSV must have a comment_text column']})
    results = []
    for _, row in df.iterrows():
        comment  = str(row['comment_text'])
        analysis = agent.analyze(comment, use_rag=False)
        emotion  = analysis['final_prediction']['emotion']
        response = generator.generate(emotion, 'bengali')
        results.append({
            'Comment':    comment[:60] + ('...' if len(comment) > 60 else ''),
            'Emotion':    emotion,
            'Confidence': f"{analysis['final_prediction']['confidence']:.0%}",
            'Decision':   analysis['final_prediction']['decision'],
            'Reply':      (response['response_text'] or 'No reply')[:60]
        })
    return pd.DataFrame(results)

# =============================================================================
# GRADIO INTERFACE
# =============================================================================

with gr.Blocks(title="CommentIQ", theme=gr.themes.Soft()) as demo:

    gr.Markdown("""
    # CommentIQ — Emotional Intelligence for Facebook Comments
    Bengali / English / Romanized-Bengali · XLM-RoBERTa + RAG + 5 Agentic Tools
    """)

    shared_chat    = gr.State([])
    selected_id_box = gr.State("")

    # -------------------------------------------------------------------------
    # TAB 1: USER PANEL
    # -------------------------------------------------------------------------
    with gr.Tab("User panel"):
        gr.Markdown("### Facebook comment section — post a comment and see the brand reply")

        user_chatbot = gr.Chatbot(
            label="Comment thread",
            height=380,
            type="messages"
        )
        user_status = gr.Textbox(
            label="Status",
            interactive=False,
            lines=1
        )
        with gr.Row():
            user_input = gr.Textbox(
                placeholder="Write a comment...",
                label="Your comment",
                lines=2,
                scale=4
            )
            user_lang = gr.Radio(
                choices=['bengali', 'english'],
                value='bengali',
                label="Reply language",
                scale=1
            )
        user_btn = gr.Button("Post comment", variant="primary")

        gr.Examples(
            examples=[
                ["দারুণ product! আবার কিনবো ❤️",        "bengali"],
                ["বাহ কি সুন্দর 🙄",                     "bengali"],
                ["darun na bhai",                         "bengali"],
                ["আপনি ভালো আছেন তো?",                  "bengali"],
                ["ডেলিভারি চার্জ কত?",                   "bengali"],
                ["how much does it cost?",                "english"],
                ["not happy with the service at all",     "english"],
                ["Visit my page for free gifts!!!",       "english"],
                ["গাজাখোর তুমি",                         "bengali"],
            ],
            inputs=[user_input, user_lang]
        )

        user_btn.click(
            user_post_comment,
            inputs=[user_input, user_lang, shared_chat],
            outputs=[user_chatbot, user_input, user_status]
        ).then(
            lambda c: c,
            inputs=[user_chatbot],
            outputs=[shared_chat]
        )

    # -------------------------------------------------------------------------
    # TAB 2: ADMIN INBOX
    # -------------------------------------------------------------------------
    with gr.Tab("Admin inbox"):
        gr.Markdown("### Pending messages — review, edit and send replies")

        with gr.Row():
            inbox_refresh_btn = gr.Button("Refresh inbox", scale=1)
            inbox_status      = gr.Textbox(
                label="Status", interactive=False, scale=3
            )

        inbox_table = gr.Dataframe(
            label="Pending messages (click a row to review)",
            value=get_inbox_df(),
            interactive=False,
            wrap=True
        )

        gr.Markdown("---")
        gr.Markdown("### Message review")

        with gr.Row():
            with gr.Column(scale=1):
                selected_comment = gr.Textbox(
                    label="User comment",
                    interactive=False,
                    lines=3
                )
                ai_summary = gr.Textbox(
                    label="AI analysis",
                    interactive=False,
                    lines=10
                )
                emotion_badge = gr.Textbox(
                    label="Detection result",
                    interactive=False,
                    lines=1
                )

            with gr.Column(scale=1):
                gr.Markdown("### Compose reply")
                reply_input = gr.Textbox(
                    label="Reply (edit if needed)",
                    lines=5,
                    placeholder="Suggested reply will appear here..."
                )
                send_btn = gr.Button("Send reply", variant="primary")
                gr.Markdown("""
                **Decision guide:**
                - >= 60% confidence → AUTO_REPLY (already sent)
                - 40–59% → HUMAN_REVIEW (you are here)
                - < 40% → FLAG_LOW_CONFIDENCE
                - Spam → NO_REPLY
                """)

        hidden_id = gr.Textbox(visible=False)

        inbox_table.select(
            load_inbox_message,
            inputs=None,
            outputs=[hidden_id, selected_comment, ai_summary, reply_input, emotion_badge]
        )

        send_btn.click(
            send_admin_reply,
            inputs=[hidden_id, reply_input, shared_chat],
            outputs=[user_chatbot, inbox_table, inbox_status]
        ).then(
            lambda c: c,
            inputs=[user_chatbot],
            outputs=[shared_chat]
        )

        inbox_refresh_btn.click(
            lambda: get_inbox_df(),
            outputs=[inbox_table]
        )

    # -------------------------------------------------------------------------
    # TAB 3: HISTORY
    # -------------------------------------------------------------------------
    with gr.Tab("History"):
        gr.Markdown("### All comments and replies — auto and manual")

        history_refresh_btn = gr.Button("Refresh history")
        history_table = gr.Dataframe(
            label="Full history",
            value=get_history_df(),
            interactive=False,
            wrap=True
        )

        history_refresh_btn.click(
            refresh_history,
            outputs=[history_table]
        )

    # -------------------------------------------------------------------------
    # TAB 4: BATCH ANALYSIS
    # -------------------------------------------------------------------------
    with gr.Tab("Batch analysis"):
        gr.Markdown("### Upload a CSV and analyze all comments at once")

        with gr.Row():
            batch_file = gr.File(
                label="Upload CSV (must have 'comment_text' column)",
                file_types=['.csv'],
                scale=2
            )
            batch_btn = gr.Button("Analyze all", scale=1)

        batch_output = gr.Dataframe(
            label="Results",
            wrap=True
        )

        gr.Markdown("""
        **CSV format:**
```
        comment_text
        দারুণ product!
        বাহ কি সুন্দর 🙄
        how much does it cost?
        Visit my page for free gifts!!!
```
        """)

        batch_btn.click(
            batch_analysis,
            inputs=[batch_file],
            outputs=[batch_output]
        )

    # -------------------------------------------------------------------------
    # FOOTER
    # -------------------------------------------------------------------------
    gr.Markdown("""
    ---
    **Type-2 model:** XLM-RoBERTa fully fine-tuned · 838 comments · F1=0.55 · best at Epoch 8

    **Type-1 agentic tools:** RAG (FAISS) · Cultural context DB · Negation detector · Spam detector · Question detector

    **Decision routing:** AUTO_REPLY (>=60%) · HUMAN_REVIEW (40–59%) · FLAG_LOW_CONFIDENCE (<40%) · NO_REPLY (spam)

    Built in 5 days · Khulna, Bangladesh
    """)

# =============================================================================
# LAUNCH
# =============================================================================

if __name__ == "__main__":
    demo.launch(
        share=True,
        server_name="0.0.0.0",
        server_port=7860
    )