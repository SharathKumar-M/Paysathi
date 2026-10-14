from app.schemas import SaathiRequest, SaathiResponse

# Curated fallback knowledge base: concise, safety-first, and available without an LLM key.
CONTENT = {
    "en": {
        "home": ("Hello, I am Saathi. I can explain a screen or help check a suspicious payment. Never share your UPI PIN or OTP with anyone.", "ask-saathi", "ask_a_question"),
        "pay": ("I will help you check this payment. Tell me why you are paying, then check the recipient and amount. Pause if anyone is rushing or threatening you. I will never move money for you.", "payment-purpose", "check_payment"),
        "message": ("Paste the message or upload a screenshot for review. I can point out warning patterns, but cannot prove who sent it. Never share an OTP or PIN.", "message-input", "explain_message"),
        "gym": ("This is practice with fake money. Read the situation, choose the safest response, and I will explain why. No real payment will happen.", "start-practice", "start_scam_gym"),
        "after": ("If money has already left your account, contact your bank immediately and call 1930. Keep relevant evidence and use the official cybercrime portal to report it.", "call-1930", "open_after_kit"),
        "simple": "Let's do one step at a time. Pause if anyone is pressuring you. Never tell anyone your PIN or OTP.",
        "otp": "Never share your OTP or UPI PIN with anyone, including someone claiming to be from a bank or the government.",
        "already_paid": "Act quickly: contact your bank using its official number and call 1930 to report suspected financial cyber fraud.",
        "greeting": "Hello! Tell me what you are trying to do, and I will guide you one step at a time.",
        "fallback": "I can help with UPI basics, checking suspicious messages, reporting suspected cyber fraud, and practising scam scenarios. What would you like help with?",
    },
    "kn": {
        "home": ("ನಮಸ್ಕಾರ, ನಾನು ಸಾಥಿ. ಈ ಪರದೆಯನ್ನು ಅರ್ಥಮಾಡಿಕೊಳ್ಳಲು ಅಥವಾ ಅನುಮಾನಾಸ್ಪದ ಪಾವತಿಯನ್ನು ಪರಿಶೀಲಿಸಲು ಸಹಾಯ ಮಾಡುತ್ತೇನೆ. ನಿಮ್ಮ UPI PIN ಅಥವಾ OTP ಅನ್ನು ಯಾರಿಗೂ ಹೇಳಬೇಡಿ.", "ask-saathi", "ask_a_question"),
        "pay": ("ಈ ಪಾವತಿಯನ್ನು ಪರಿಶೀಲಿಸಲು ಸಹಾಯ ಮಾಡುತ್ತೇನೆ. ಏಕೆ ಪಾವತಿಸುತ್ತಿದ್ದೀರಿ ಎಂದು ತಿಳಿಸಿ; ಸ್ವೀಕರಿಸುವವರ ಹೆಸರು ಮತ್ತು ಮೊತ್ತವನ್ನು ಪರಿಶೀಲಿಸಿ. ಯಾರಾದರೂ ಆತುರಪಡಿಸಿದರೆ ನಿಲ್ಲಿಸಿ. ನಾನು ಹಣ ವರ್ಗಾಯಿಸುವುದಿಲ್ಲ.", "payment-purpose", "check_payment"),
        "message": ("ಸಂದೇಶವನ್ನು ಅಂಟಿಸಿ ಅಥವಾ ಸ್ಕ್ರೀನ್‌ಶಾಟ್ ಪರಿಶೀಲನೆಗೆ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ. ಅನುಮಾನಾಸ್ಪದ ಲಕ್ಷಣಗಳನ್ನು ತಿಳಿಸಬಹುದು, ಆದರೆ ಕಳುಹಿಸಿದವರನ್ನು ಖಚಿತಪಡಿಸಲು ಸಾಧ್ಯವಿಲ್ಲ. OTP ಅಥವಾ PIN ಹಂಚಿಕೊಳ್ಳಬೇಡಿ.", "message-input", "explain_message"),
        "gym": ("ಇದು ನಕಲಿ ಹಣದೊಂದಿಗೆ ಅಭ್ಯಾಸ. ಪರಿಸ್ಥಿತಿಯನ್ನು ಓದಿ ಸುರಕ್ಷಿತ ಆಯ್ಕೆಯನ್ನು ಆರಿಸಿ. ಯಾವುದೇ ನಿಜವಾದ ಪಾವತಿ ನಡೆಯುವುದಿಲ್ಲ.", "start-practice", "start_scam_gym"),
        "after": ("ಹಣ ಈಗಾಗಲೇ ಕಡಿತವಾಗಿದ್ದರೆ, ತಕ್ಷಣ ನಿಮ್ಮ ಬ್ಯಾಂಕ್ ಅನ್ನು ಸಂಪರ್ಕಿಸಿ ಮತ್ತು ಹಣಕಾಸು ಸೈಬರ್ ವಂಚನೆಯನ್ನು ವರದಿ ಮಾಡಲು 1930 ಗೆ ಕರೆ ಮಾಡಿ.", "call-1930", "open_after_kit"),
        "simple": "ಒಂದು ಸಮಯದಲ್ಲಿ ಒಂದು ಹೆಜ್ಜೆ ಮಾಡಿ. ಯಾರಾದರೂ ಒತ್ತಡ ಹಾಕಿದರೆ ನಿಲ್ಲಿಸಿ. PIN ಅಥವಾ OTP ಯಾರಿಗೂ ಹೇಳಬೇಡಿ.",
        "otp": "ನಿಮ್ಮ OTP ಅಥವಾ UPI PIN ಅನ್ನು ಬ್ಯಾಂಕ್ ಅಥವಾ ಸರ್ಕಾರದವರು ಎಂದು ಹೇಳುವ ವ್ಯಕ್ತಿಗೂ ಹಂಚಿಕೊಳ್ಳಬೇಡಿ.",
        "already_paid": "ತಕ್ಷಣ ಕ್ರಮ ಕೈಗೊಳ್ಳಿ: ಬ್ಯಾಂಕಿನ ಅಧಿಕೃತ ಸಂಖ್ಯೆಗೆ ಸಂಪರ್ಕಿಸಿ ಮತ್ತು ವಂಚನೆಯನ್ನು ವರದಿ ಮಾಡಲು 1930 ಗೆ ಕರೆ ಮಾಡಿ.",
        "greeting": "ನಮಸ್ಕಾರ! ನೀವು ಏನು ಮಾಡಲು ಪ್ರಯತ್ನಿಸುತ್ತಿದ್ದೀರಿ ಎಂದು ಹೇಳಿ. ಒಂದೊಂದು ಹೆಜ್ಜೆಯಾಗಿ ಸಹಾಯ ಮಾಡುತ್ತೇನೆ.",
        "fallback": "UPI, ಅನುಮಾನಾಸ್ಪದ ಸಂದೇಶ, ಸೈಬರ್ ವಂಚನೆ ವರದಿ ಮತ್ತು ವಂಚನೆ ಗುರುತಿಸುವ ಅಭ್ಯಾಸದಲ್ಲಿ ಸಹಾಯ ಮಾಡುತ್ತೇನೆ. ನಿಮಗೆ ಯಾವ ಸಹಾಯ ಬೇಕು?",
    },
    "hi": {
        "home": ("नमस्ते, मैं साथी हूँ। मैं स्क्रीन समझने या संदिग्ध भुगतान जाँचने में मदद कर सकता हूँ। अपना UPI PIN या OTP किसी को न बताएं।", "ask-saathi", "ask_a_question"),
        "pay": ("मैं इस भुगतान को जाँचने में मदद करूँगा। बताइए कि आप भुगतान क्यों कर रहे हैं। प्राप्तकर्ता और राशि जाँचें; कोई जल्दी या धमकी दे तो रुकें। मैं आपके लिए पैसे नहीं भेजता।", "payment-purpose", "check_payment"),
        "message": ("संदेश का टेक्स्ट पेस्ट करें या स्क्रीनशॉट जाँच के लिए अपलोड करें। मैं चेतावनी के संकेत बता सकता हूँ, लेकिन भेजने वाले की पहचान साबित नहीं कर सकता। OTP या PIN साझा न करें।", "message-input", "explain_message"),
        "gym": ("यह नकली पैसे से अभ्यास है। स्थिति पढ़ें, सुरक्षित विकल्प चुनें और मैं कारण समझाऊँगा। कोई असली भुगतान नहीं होगा।", "start-practice", "start_scam_gym"),
        "after": ("अगर पैसे कट गए हैं, तो तुरंत अपने बैंक से संपर्क करें और वित्तीय साइबर धोखाधड़ी की रिपोर्ट के लिए 1930 पर कॉल करें।", "call-1930", "open_after_kit"),
        "simple": "एक बार में एक कदम करें। कोई दबाव डाले तो रुकें। अपना PIN या OTP किसी को न बताएं।",
        "otp": "अपना OTP या UPI PIN किसी को न बताएं, भले ही वह बैंक या सरकारी अधिकारी होने का दावा करे।",
        "already_paid": "जल्दी कार्रवाई करें: बैंक के आधिकारिक नंबर पर संपर्क करें और संदिग्ध वित्तीय साइबर धोखाधड़ी की रिपोर्ट के लिए 1930 पर कॉल करें।",
        "greeting": "नमस्ते! बताइए कि आप क्या करना चाहते हैं। मैं एक-एक कदम में मदद करूँगा।",
        "fallback": "मैं UPI, संदिग्ध संदेशों, साइबर धोखाधड़ी की रिपोर्ट और सुरक्षित अभ्यास में मदद कर सकता हूँ। आपको क्या जानना है?",
    },
}


def answer_saathi(request: SaathiRequest) -> SaathiResponse:
    pack = CONTENT[request.language]
    screen = request.current_screen.lower().replace("_", "-")
    msg = request.message.strip().lower()
    if request.simplify:
        return SaathiResponse(answer=pack["simple"], language=request.language, next_action="continue_step_by_step")
    if any(k in msg for k in ("otp", "pin", "password", "secret code")):
        return SaathiResponse(answer=pack["otp"], language=request.language, next_action="do_not_share_secret")
    if any(k in msg for k in ("already paid", "money cut", "money deducted", "sent money", "lost money", "fraud happened", "ಹಣ ಕಡಿತ", "पैसे कट")):
        return SaathiResponse(answer=pack["already_paid"], language=request.language, highlight_element="call-1930", next_action="open_after_kit")
    if not msg or msg in {"hi", "hello", "help", "namaste", "ನಮಸ್ಕಾರ", "नमस्ते"}:
        answer, highlight, action = {"pay-guard": pack["pay"], "payment": pack["pay"], "message-explainer": pack["message"], "scam-gym": pack["gym"], "after-kit": pack["after"]}.get(screen, pack["home"])
        return SaathiResponse(answer=answer, language=request.language, highlight_element=highlight, next_action=action, suggestions=["Check a payment", "Explain a message", "Practice a scam"])
    if screen in {"pay-guard", "pay", "payment", "intent-aware-pay-guard"} or any(k in msg for k in ("pay", "payment", "upi", "qr", "transfer")):
        answer, highlight, action = pack["pay"]
    elif screen in {"message-explainer", "message", "messages"} or any(k in msg for k in ("message", "sms", "whatsapp", "link", "bank alert")):
        answer, highlight, action = pack["message"]
    elif screen in {"scam-gym", "gym", "practice"} or any(k in msg for k in ("practice", "learn scam", "training")):
        answer, highlight, action = pack["gym"]
    elif screen in {"after-kit", "after", "recovery", "report"}:
        answer, highlight, action = pack["after"]
    elif any(k in msg for k in ("who are you", "hello", "hi saathi")):
        answer, highlight, action = pack["greeting"], "ask-saathi", "ask_a_question"
    else:
        answer, highlight, action = pack["fallback"], None, "choose_supported_topic"
    return SaathiResponse(answer=answer, language=request.language, highlight_element=highlight, next_action=action, suggestions=["Check a payment", "Explain a message", "Report suspected fraud"])
