from app.schemas import AfterKitRequest, AfterKitResponse

TEXT = {
    "en": {
        "urgent_headline": "Act quickly if money has left your account",
        "prevention_headline": "Pause and verify before paying",
        "caution_headline": "Do not continue until you verify",
        "paid_steps": [
            "Call your bank using the official number from its app, card, or website. Report suspected fraud and ask whether the transaction can be stopped or flagged.",
            "Call 1930 as soon as possible to report financial cyber fraud. Keep the acknowledgement/reference number.",
            "Submit the report at cybercrime.gov.in and follow the official instructions.",
            "Do not call back the suspected scammer or share an OTP, PIN, password, or remote-access code.",
        ],
        "not_paid_steps": [
            "Do not approve the payment or send more money.",
            "End any unexpected call. Do not use links or phone numbers sent by the caller.",
            "Check the claim through the official bank/service app, website, or a phone number you find independently.",
        ],
        "unsure_steps": [
            "Pause. Do not approve any new payment or share an OTP/PIN.",
            "Check your bank app directly for a debit. If money has left your account, call your bank and 1930 immediately.",
            "Verify the request using an official contact you find independently.",
        ],
        "evidence": ["Screenshot of the suspicious message or call log, if available", "Caller/sender number or profile", "Transaction ID/UTR, date, time and amount from official bank/payment history", "Relevant payment receipt or bank alert"],
        "bank_script": "Hello, I suspect I have been targeted by financial cyber fraud. The transaction amount is {amount}. Please register my complaint, check whether the transaction can be stopped or flagged, secure my account if needed, and give me a complaint/reference number. I am also reporting it to 1930.",
    },
    "kn": {
        "urgent_headline": "ನಿಮ್ಮ ಖಾತೆಯಿಂದ ಹಣ ಕಡಿತವಾಗಿದ್ದರೆ ತಕ್ಷಣ ಕ್ರಮ ಕೈಗೊಳ್ಳಿ",
        "prevention_headline": "ಪಾವತಿಸುವ ಮೊದಲು ನಿಲ್ಲಿಸಿ ಪರಿಶೀಲಿಸಿ",
        "caution_headline": "ಪರಿಶೀಲಿಸುವವರೆಗೆ ಮುಂದುವರಿಯಬೇಡಿ",
        "paid_steps": ["ಬ್ಯಾಂಕಿನ ಅಧಿಕೃತ ಆ್ಯಪ್, ಕಾರ್ಡ್ ಅಥವಾ ವೆಬ್‌ಸೈಟ್‌ನಲ್ಲಿರುವ ಸಂಖ್ಯೆಗೆ ಕರೆ ಮಾಡಿ. ವಂಚನೆಯ ಶಂಕೆಯನ್ನು ತಿಳಿಸಿ, ವ್ಯವಹಾರವನ್ನು ತಡೆಯಲು ಸಾಧ್ಯವೇ ಎಂದು ಕೇಳಿ.", "ಹಣಕಾಸು ಸೈಬರ್ ವಂಚನೆಯನ್ನು ವರದಿ ಮಾಡಲು ಸಾಧ್ಯವಾದಷ್ಟು ಬೇಗ 1930 ಗೆ ಕರೆ ಮಾಡಿ. ಉಲ್ಲೇಖ ಸಂಖ್ಯೆಯನ್ನು ಉಳಿಸಿಕೊಳ್ಳಿ.", "cybercrime.gov.in ನಲ್ಲಿ ವರದಿ ಸಲ್ಲಿಸಿ ಮತ್ತು ಅಧಿಕೃತ ಸೂಚನೆಗಳನ್ನು ಅನುಸರಿಸಿ.", "ಶಂಕಿತ ವ್ಯಕ್ತಿಗೆ ಮರಳಿ ಕರೆ ಮಾಡಬೇಡಿ; OTP, PIN, ಪಾಸ್‌ವರ್ಡ್ ಅಥವಾ ರಿಮೋಟ್-ಆಕ್ಸೆಸ್ ಕೋಡ್ ಹಂಚಿಕೊಳ್ಳಬೇಡಿ."],
        "not_paid_steps": ["ಪಾವತಿಯನ್ನು ಅನುಮೋದಿಸಬೇಡಿ ಅಥವಾ ಇನ್ನಷ್ಟು ಹಣ ಕಳುಹಿಸಬೇಡಿ.", "ಅನಿರೀಕ್ಷಿತ ಕರೆಯನ್ನು ಮುಗಿಸಿ. ಕರೆ ಮಾಡಿದವರು ಕಳುಹಿಸಿದ ಲಿಂಕ್ ಅಥವಾ ಸಂಖ್ಯೆಯನ್ನು ಬಳಸಬೇಡಿ.", "ಅಧಿಕೃತ ಬ್ಯಾಂಕ್/ಸೇವಾ ಆ್ಯಪ್, ವೆಬ್‌ಸೈಟ್ ಅಥವಾ ನೀವೇ ಹುಡುಕಿದ ಸಂಖ್ಯೆಯ ಮೂಲಕ ಪರಿಶೀಲಿಸಿ."],
        "unsure_steps": ["ನಿಲ್ಲಿಸಿ. ಹೊಸ ಪಾವತಿಯನ್ನು ಅನುಮೋದಿಸಬೇಡಿ ಅಥವಾ OTP/PIN ಹಂಚಿಕೊಳ್ಳಬೇಡಿ.", "ಬ್ಯಾಂಕ್ ಆ್ಯಪ್‌ನಲ್ಲಿ ಹಣ ಕಡಿತವಾಗಿದೆಯೇ ಪರಿಶೀಲಿಸಿ. ಹಣ ಕಡಿತವಾಗಿದ್ದರೆ ತಕ್ಷಣ ಬ್ಯಾಂಕ್ ಮತ್ತು 1930 ಅನ್ನು ಸಂಪರ್ಕಿಸಿ.", "ನೀವೇ ಕಂಡುಕೊಂಡ ಅಧಿಕೃತ ಸಂಪರ್ಕದ ಮೂಲಕ ವಿನಂತಿಯನ್ನು ಪರಿಶೀಲಿಸಿ."],
        "evidence": ["ಸಂದೇಶ ಅಥವಾ ಕರೆ ದಾಖಲೆಯ ಸ್ಕ್ರೀನ್‌ಶಾಟ್, ಇದ್ದರೆ", "ಕರೆ ಮಾಡಿದವರ/ಕಳುಹಿಸಿದವರ ಸಂಖ್ಯೆ ಅಥವಾ ಪ್ರೊಫೈಲ್", "ಅಧಿಕೃತ ವ್ಯವಹಾರ ಇತಿಹಾಸದಿಂದ Transaction ID/UTR, ದಿನಾಂಕ, ಸಮಯ ಮತ್ತು ಮೊತ್ತ", "ಪಾವತಿ ರಸೀದಿ ಅಥವಾ ಬ್ಯಾಂಕ್ ಎಚ್ಚರಿಕೆ"],
        "bank_script": "ನಮಸ್ಕಾರ, ನಾನು ಹಣಕಾಸು ಸೈಬರ್ ವಂಚನೆಯ ಶಂಕೆ ಹೊಂದಿದ್ದೇನೆ. ವ್ಯವಹಾರದ ಮೊತ್ತ {amount}. ದಯವಿಟ್ಟು ನನ್ನ ದೂರು ದಾಖಲಿಸಿ, ವ್ಯವಹಾರವನ್ನು ತಡೆಯಲು ಸಾಧ್ಯವೇ ಪರಿಶೀಲಿಸಿ, ಅಗತ್ಯವಿದ್ದರೆ ಖಾತೆಯನ್ನು ಸುರಕ್ಷಿತಗೊಳಿಸಿ ಮತ್ತು ದೂರು ಉಲ್ಲೇಖ ಸಂಖ್ಯೆಯನ್ನು ನೀಡಿ. ನಾನು 1930 ಕ್ಕೂ ವರದಿ ಮಾಡುತ್ತಿದ್ದೇನೆ.",
    },
    "hi": {
        "urgent_headline": "अगर खाते से पैसे कटे हैं, तो तुरंत कार्रवाई करें",
        "prevention_headline": "भुगतान से पहले रुकें और जाँचें",
        "caution_headline": "जाँच होने तक आगे न बढ़ें",
        "paid_steps": ["अपने बैंक के आधिकारिक ऐप, कार्ड या वेबसाइट पर दिए गए नंबर पर कॉल करें। संदिग्ध धोखाधड़ी बताएँ और पूछें कि लेन-देन रोका जा सकता है या नहीं।", "वित्तीय साइबर धोखाधड़ी की रिपोर्ट के लिए जल्द से जल्द 1930 पर कॉल करें और संदर्भ नंबर सुरक्षित रखें।", "cybercrime.gov.in पर रिपोर्ट जमा करें और आधिकारिक निर्देशों का पालन करें।", "संदिग्ध व्यक्ति को वापस कॉल न करें और OTP, PIN, पासवर्ड या रिमोट-एक्सेस कोड साझा न करें।"],
        "not_paid_steps": ["भुगतान मंज़ूर न करें और अतिरिक्त पैसे न भेजें।", "अनजान कॉल समाप्त करें। कॉल करने वाले के भेजे लिंक या नंबर का उपयोग न करें।", "बैंक/सेवा के आधिकारिक ऐप, वेबसाइट या खुद ढूँढे गए नंबर से जाँच करें।"],
        "unsure_steps": ["रुकें। कोई नया भुगतान मंज़ूर न करें और OTP/PIN साझा न करें।", "बैंक ऐप सीधे खोलकर जाँचें कि पैसे कटे हैं या नहीं। पैसे कटे हों तो तुरंत बैंक और 1930 से संपर्क करें।", "खुद ढूँढे गए आधिकारिक संपर्क से अनुरोध की पुष्टि करें।"],
        "evidence": ["संदिग्ध संदेश या कॉल लॉग का स्क्रीनशॉट, यदि उपलब्ध हो", "कॉलर/भेजने वाले का नंबर या प्रोफ़ाइल", "आधिकारिक भुगतान इतिहास से Transaction ID/UTR, तारीख, समय और राशि", "भुगतान रसीद या बैंक अलर्ट"],
        "bank_script": "नमस्ते, मुझे वित्तीय साइबर धोखाधड़ी का संदेह है। लेन-देन की राशि {amount} है। कृपया मेरी शिकायत दर्ज करें, जाँचें कि लेन-देन रोका जा सकता है या नहीं, आवश्यकता हो तो खाते को सुरक्षित करें और शिकायत संदर्भ संख्या दें। मैं 1930 पर भी रिपोर्ट कर रहा/रही हूँ।",
    },
}


def build_after_kit(request: AfterKitRequest) -> AfterKitResponse:
    t = TEXT[request.language]
    amount = f"₹{request.amount:,.2f}" if request.amount is not None else "[transaction amount]"
    if request.incident_status == "paid":
        urgency, headline, steps = "urgent", t["urgent_headline"], t["paid_steps"]
    elif request.incident_status == "not_paid":
        urgency, headline, steps = "prevention", t["prevention_headline"], t["not_paid_steps"]
    else:
        urgency, headline, steps = "caution", t["caution_headline"], t["unsure_steps"]
    available = {
        "screenshot": request.has_screenshot,
        "caller_number": request.has_caller_number,
        "transaction_details": request.has_transaction_details,
    }
    labels = {
        "en": {
            "screenshot": "Screenshot of the suspicious message or call log",
            "caller_number": "Caller/sender number or profile",
            "transaction_details": "Transaction ID/UTR, date, time and amount from official bank/payment history",
            "receipt": "Relevant payment receipt or bank alert",
            "available": "Marked as available on your device: ",
            "missing": "If available and safe, collect: ",
        },
        "kn": {
            "screenshot": "ಸಂದೇಶ ಅಥವಾ ಕರೆ ದಾಖಲೆಯ ಸ್ಕ್ರೀನ್‌ಶಾಟ್",
            "caller_number": "ಕರೆ ಮಾಡಿದವರ/ಕಳುಹಿಸಿದವರ ಸಂಖ್ಯೆ ಅಥವಾ ಪ್ರೊಫೈಲ್",
            "transaction_details": "ಅಧಿಕೃತ ಪಾವತಿ ಇತಿಹಾಸದಿಂದ Transaction ID/UTR, ದಿನಾಂಕ, ಸಮಯ ಮತ್ತು ಮೊತ್ತ",
            "receipt": "ಪಾವತಿ ರಸೀದಿ ಅಥವಾ ಬ್ಯಾಂಕ್ ಎಚ್ಚರಿಕೆ",
            "available": "ನಿಮ್ಮ ಸಾಧನದಲ್ಲಿ ಲಭ್ಯವೆಂದು ಗುರುತಿಸಲಾಗಿದೆ: ",
            "missing": "ಲಭ್ಯವಿದ್ದರೆ ಮತ್ತು ಸುರಕ್ಷಿತವಾಗಿದ್ದರೆ ಸಂಗ್ರಹಿಸಿ: ",
        },
        "hi": {
            "screenshot": "संदिग्ध संदेश या कॉल लॉग का स्क्रीनशॉट",
            "caller_number": "कॉलर/भेजने वाले का नंबर या प्रोफ़ाइल",
            "transaction_details": "आधिकारिक भुगतान इतिहास से Transaction ID/UTR, तारीख, समय और राशि",
            "receipt": "भुगतान रसीद या बैंक अलर्ट",
            "available": "आपके डिवाइस पर उपलब्ध के रूप में चिह्नित: ",
            "missing": "यदि उपलब्ध और सुरक्षित हो, तो यह जुटाएँ: ",
        },
    }[request.language]
    evidence = []
    for key in ("screenshot", "caller_number", "transaction_details"):
        prefix = labels["available"] if available[key] else labels["missing"]
        evidence.append(prefix + labels[key])
    evidence.append(labels["missing"] + labels["receipt"])
    return AfterKitResponse(
        urgency=urgency,
        headline=headline,
        steps=steps,
        evidence_checklist=evidence,
        bank_call_script=t["bank_script"].format(amount=amount),
    )
