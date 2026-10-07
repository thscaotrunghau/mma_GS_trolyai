// ---------------------------------------------------------
// PHIÊN BẢN CHUYÊN DỤNG CHO GOOGLE SLIDES (TỐI ƯU TỰ ĐỘNG MỞ)
// ---------------------------------------------------------

// Tự động chạy khi mở file
function onOpen() {
  var ui = SlidesApp.getUi();
  
  // Tạo Menu
  ui.createMenu('MMA - Trợ Lý AI GS')
    .addItem('Mở Trợ lý', 'showSidebar')
    .addToUi();
    
  // Tự động bật Sidebar mà không bị Google chặn
  try {
    showSidebar();
  } catch(e) {}
}

// Hàm mở thanh Sidebar bên phải
function showSidebar() {
  var ui = SlidesApp.getUi();
  var html = HtmlService.createHtmlOutputFromFile('Sidebar')
      .setTitle('MMA - Trợ Lý AI GS')
      .setWidth(300);
  ui.showSidebar(html);
}

// Lấy văn bản đang bôi đen trên Slide
function getSelectedText() {
  var selection = SlidesApp.getActivePresentation().getSelection();
  if (selection) {
    var selectionType = selection.getSelectionType();
    if (selectionType == SlidesApp.SelectionType.TEXT) {
      return selection.getTextRange().asString();
    } else if (selectionType == SlidesApp.SelectionType.PAGE_ELEMENT) {
      var elements = selection.getPageElementRange().getPageElements();
      var texts = [];
      for (var i = 0; i < elements.length; i++) {
        if (elements[i].getPageElementType() == SlidesApp.PageElementType.SHAPE) {
          texts.push(elements[i].asShape().getText().asString());
        }
      }
      return texts.join('\n');
    }
  }
  return '';
}

// Lấy toàn bộ văn bản trong Slide (nếu không bôi đen)
function getFullText() {
  var slides = SlidesApp.getActivePresentation().getSlides();
  var texts = [];
  for (var i = 0; i < slides.length; i++) {
    var shapes = slides[i].getShapes();
    for (var j = 0; j < shapes.length; j++) {
      texts.push(shapes[j].getText().asString());
    }
  }
  return texts.join('\n');
}

// Kết nối với API của DeepSeek
function callDeepSeekAPI(prompt, apiKey) {
  var url = "https://api.deepseek.com/chat/completions";
  var payload = {
    "model": "deepseek-chat",
    "messages": [
      {"role": "system", "content": "You are a friendly and enthusiastic assistant. IMPORTANT RULES: Do NOT use any markdown formatting like asterisks (**) or hashes (#). Use plain text only. Use lots of lively emojis to make the response engaging, cute, and easy to read. Write naturally as if talking to a friend."},
      {"role": "user", "content": prompt}
    ],
    "temperature": 0.7 
  };
  
  var options = {
    "method": "post",
    "headers": {
      "Authorization": "Bearer " + apiKey,
      "Content-Type": "application/json"
    },
    "payload": JSON.stringify(payload),
    "muteHttpExceptions": true
  };
  
  var response = UrlFetchApp.fetch(url, options);
  var json = JSON.parse(response.getContentText());
  
  if (json.error) {
    throw new Error(json.error.message);
  }
  
  return json.choices[0].message.content;
}

// Xử lý logic từ Sidebar
function processRequest(action, apiKey, targetLang) {
  PropertiesService.getUserProperties().setProperty('DEEPSEEK_API_KEY', apiKey);
  
  var text = getSelectedText();
  if (!text) {
    text = getFullText(); 
    if (!text || text.trim() === '') {
      return JSON.stringify({ error: "Lỗi: Mình không tìm thấy nội dung nào cả! Bạn hãy thử bôi đen một đoạn nhé. 😅" });
    }
    if (text.length > 15000) {
      text = text.substring(0, 15000) + "...";
    }
  }
  
  var prompt = "";
  if (action === 'translate') {
    prompt = "Hãy dịch nội dung sau sang " + targetLang + " một cách tự nhiên, dễ hiểu nhất:\n\n" + text;
  } else if (action === 'explain') {
    prompt = "Hãy giải thích thật chi tiết, rõ ràng và dễ hiểu các khái niệm hoặc ý chính trong nội dung sau bằng " + targetLang + ":\n\n" + text;
  } else if (action === 'summarize') {
    prompt = "Hãy tóm tắt ngắn gọn những ý chính quan trọng nhất của nội dung sau bằng " + targetLang + ":\n\n" + text;
  }
  
  try {
    var response = callDeepSeekAPI(prompt, apiKey);
    return JSON.stringify({
      originalText: text,
      aiResponse: response
    });
  } catch(e) {
    return JSON.stringify({ error: "❌ Lỗi: " + e.message });
  }
}

function getSavedApiKey() {
  return PropertiesService.getUserProperties().getProperty('DEEPSEEK_API_KEY') || '';
}

// --- BỔ SUNG CHO CHẾ ĐỘ TỰ ĐỘNG THUYẾT TRÌNH (AUTO PRESENTER) ---

// Lấy toàn bộ văn bản của tất cả các slide
function getAllSlidesData() {
  try {
    var pres = SlidesApp.getActivePresentation();
    var slides = pres.getSlides();
    var data = [];
    
    for (var i = 0; i < slides.length; i++) {
      var elements = slides[i].getPageElements();
      var textArr = [];
      for (var j = 0; j < elements.length; j++) {
        if (elements[j].getPageElementType() == SlidesApp.PageElementType.SHAPE) {
          var text = elements[j].asShape().getText().asString().trim();
          if (text) textArr.push(text);
        }
      }
      data.push({
        slideIndex: i,
        text: textArr.join('\n\n')
      });
    }
    return JSON.stringify(data);
  } catch (e) {
    return JSON.stringify({error: e.toString()});
  }
}

// Chuyển tới slide số chỉ định
function goToSlide(index) {
  try {
    var pres = SlidesApp.getActivePresentation();
    var slides = pres.getSlides();
    if (index >= 0 && index < slides.length) {
      slides[index].selectAsCurrentPage();
    }
  } catch (e) {}
}

// Gọi API dịch cho text tuỳ ý (phục vụ Auto Presenter)
function processTextDirectly(text, apiKey, targetLang) {
  try {
    if (!text || text.trim() === '') {
      return JSON.stringify({ error: "Văn bản trống." });
    }
    
    var prompt = "Hãy dịch nội dung sau sang " + targetLang + " một cách tự nhiên. CHỈ TRẢ VỀ NỘI DUNG ĐÃ DỊCH, tuyệt đối không thêm lời chào, không giải thích. Giữ nguyên cấu trúc đoạn văn bản:\n\n" + text;
    
    var response = callDeepSeekAPI(prompt, apiKey);
    return JSON.stringify({
      originalText: text,
      aiResponse: response
    });
  } catch (e) {
    return JSON.stringify({ error: "❌ Lỗi: " + e.message });
  }
}

