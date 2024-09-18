# 在 AWS 上進行物聯網與人工智慧實作
本系列文章主要結合三大元素：物聯網設備、雲端計算與人工智慧。隨著人工智慧的爆發式成長，人工智慧的應用已經遍及影像、影片、聲音、對話、文章等領域，而公有雲已經將人工智慧的開發或是應用封裝成完善的服務，對於人工智慧的模型開發者或是應用開發者而言，只需要的去熟悉、了解開發框架，就可以快速的應用人工智慧的技術，而不需要再花時間在購買GPU，安裝驅動、安裝開發框架等基礎環境搭建等無關事務上，可以專注於核心專業上。所以本系列文章以 Python 為主要開發語言， ESP32-CAM 作為物聯網設備，接著介紹 AWS 雲端基礎建設與機器學習的相關服務，最後將 AWS 文字/人臉辨識與 ESP32-CAM 進行整合，完成一個結合物聯網設備、雲端計算與人工智慧的應用系統。

**目錄**

- [在 AWS 上進行物聯網與人工智慧實作](#%E5%9C%A8-aws-%E4%B8%8A%E9%80%B2%E8%A1%8C%E7%89%A9%E8%81%AF%E7%B6%B2%E8%88%87%E4%BA%BA%E5%B7%A5%E6%99%BA%E6%85%A7%E5%AF%A6%E4%BD%9C)
    - [所需相關知識](#所需相關知識)
    - [所需資源](#所需資源)
    - [本系列文章](#本系列文章)
        - [第一部分 Python 基礎概念](#%E7%AC%AC%E4%B8%80%E9%83%A8%E5%88%86-python-%E5%9F%BA%E7%A4%8E%E6%A6%82%E5%BF%B5)
        - [第二部分 ESP32-CAM](#%E7%AC%AC%E4%BA%8C%E9%83%A8%E5%88%86-esp32-cam)
        - [第三部分 網際網路基礎](#%E7%AC%AC%E4%B8%89%E9%83%A8%E5%88%86-%E7%B6%B2%E9%9A%9B%E7%B6%B2%E8%B7%AF%E5%9F%BA%E7%A4%8E)
        - [第四部分 AWS 服務](#%E7%AC%AC%E5%9B%9B%E9%83%A8%E5%88%86-aws-%E6%9C%8D%E5%8B%99)
        - [第五部分 系統整合](#%E7%AC%AC%E4%BA%94%E9%83%A8%E5%88%86-%E7%B3%BB%E7%B5%B1%E6%95%B4%E5%90%88)


## 所需相關知識
[<img src='https://ithelp.ithome.com.tw/upload/images/20240808/20129510u6xSlclLMa.png' width='5%'></img>](#%E5%9C%A8-aws-%E4%B8%8A%E9%80%B2%E8%A1%8C%E7%89%A9%E8%81%AF%E7%B6%B2%E8%88%87%E4%BA%BA%E5%B7%A5%E6%99%BA%E6%85%A7%E5%AF%A6%E4%BD%9C) [<img src='https://ithelp.ithome.com.tw/upload/images/20240808/201295100ApjQbzYXJ.png' width='5%'></img>](#bottom)

* Python 基礎概念
* 介紹單晶片 ESP32-CAM
* 使用 MicroPython 開發ESP32-CAM
* AWS基礎設施服務
* Amazon API Gateway
* AWS Lambda
* Amazon DynamoDB
* Amazon S3
* Amazon Rekognition
* 網際網路基礎
* HTTP Request/Response

## 所需資源
[<img src='https://ithelp.ithome.com.tw/upload/images/20240808/20129510u6xSlclLMa.png' width='5%'></img>](#%E5%9C%A8-aws-%E4%B8%8A%E9%80%B2%E8%A1%8C%E7%89%A9%E8%81%AF%E7%B6%B2%E8%88%87%E4%BA%BA%E5%B7%A5%E6%99%BA%E6%85%A7%E5%AF%A6%E4%BD%9C) [<img src='https://ithelp.ithome.com.tw/upload/images/20240808/201295100ApjQbzYXJ.png' width='5%'></img>](#bottom)

* AWS 帳號 - 建議可以申請[AWS 免費方案](https://aws.amazon.com/tw/free/free-tier-faqs/) 
* 或 AWS Academy Learner Lab 帳號 - 這是針對有加入AWS Academy專案的學校，也是免費的
* ESP32-CAM 與 CH340 下載轉接頭

## 本系列文章
[<img src='https://ithelp.ithome.com.tw/upload/images/20240808/20129510u6xSlclLMa.png' width='5%'></img>](#%E5%9C%A8-aws-%E4%B8%8A%E9%80%B2%E8%A1%8C%E7%89%A9%E8%81%AF%E7%B6%B2%E8%88%87%E4%BA%BA%E5%B7%A5%E6%99%BA%E6%85%A7%E5%AF%A6%E4%BD%9C) [<img src='https://ithelp.ithome.com.tw/upload/images/20240808/201295100ApjQbzYXJ.png' width='5%'></img>](#bottom)

這本系列文章規劃成 5 個部分，從 Python 基礎開始，接著使用 ESP32-CAM 的 microPython，接著在 AWS 上使用AWS Lambda 編寫無伺服器的 Python 程式，來完成文字與人臉辨識的功能，並透過每個單元的實作讓你一步一步完成這份專案：

### 第一部分 Python 基礎概念
[<img src='https://ithelp.ithome.com.tw/upload/images/20240808/20129510u6xSlclLMa.png' width='5%'></img>](#%E5%9C%A8-aws-%E4%B8%8A%E9%80%B2%E8%A1%8C%E7%89%A9%E8%81%AF%E7%B6%B2%E8%88%87%E4%BA%BA%E5%B7%A5%E6%99%BA%E6%85%A7%E5%AF%A6%E4%BD%9C) [<img src='https://ithelp.ithome.com.tw/upload/images/20240808/201295100ApjQbzYXJ.png' width='5%'></img>](#bottom)

了解 Python 的基礎語法與開發環境
  - [Python 說明與開發環境](https://ithelp.ithome.com.tw/articles/10343895)
  - [Python 基礎語法](https://ithelp.ithome.com.tw/articles/10344068)
  - [Python 基本資料類型](https://ithelp.ithome.com.tw/articles/10344110)
  - [Python 分支控制](https://ithelp.ithome.com.tw/articles/10344336)
  - [Python 函數與模組](https://ithelp.ithome.com.tw/articles/10344487)
### 第二部分 ESP32-CAM
[<img src='https://ithelp.ithome.com.tw/upload/images/20240808/20129510u6xSlclLMa.png' width='5%'></img>](#%E5%9C%A8-aws-%E4%B8%8A%E9%80%B2%E8%A1%8C%E7%89%A9%E8%81%AF%E7%B6%B2%E8%88%87%E4%BA%BA%E5%B7%A5%E6%99%BA%E6%85%A7%E5%AF%A6%E4%BD%9C) [<img src='https://ithelp.ithome.com.tw/upload/images/20240808/201295100ApjQbzYXJ.png' width='5%'></img>](#bottom)

介紹單晶片 ESP32-CAM 的出處、結構與基礎程式應用。
  * [單晶片 ESP32-CAM](https://ithelp.ithome.com.tw/articles/10344613)
  * [使用 MicroPython 開發 ESP32-CAM - Thonny](https://ithelp.ithome.com.tw/articles/10344722)
  * [使用 MicroPython 檔案存取](https://ithelp.ithome.com.tw/articles/10344852)
  * [使用 MicroPython 控制燈號、撰寫 ISR](https://ithelp.ithome.com.tw/articles/10344998)
  * [使用 MicroPython 連接 Wi-Fi、同步 NTP](https://ithelp.ithome.com.tw/articles/10345000)
  * [使用 MicroPython 安裝新模組與使用](https://ithelp.ithome.com.tw/articles/10345284)
  * [使用 MicroPython 拍照](https://ithelp.ithome.com.tw/articles/10345443)
### 第三部分 網際網路基礎
[<img src='https://ithelp.ithome.com.tw/upload/images/20240808/20129510u6xSlclLMa.png' width='5%'></img>](#%E5%9C%A8-aws-%E4%B8%8A%E9%80%B2%E8%A1%8C%E7%89%A9%E8%81%AF%E7%B6%B2%E8%88%87%E4%BA%BA%E5%B7%A5%E6%99%BA%E6%85%A7%E5%AF%A6%E4%BD%9C) [<img src='https://ithelp.ithome.com.tw/upload/images/20240808/201295100ApjQbzYXJ.png' width='5%'></img>](#bottom)

說明網頁運作基本原理。
  - [網際網路模型](https://ithelp.ithome.com.tw/articles/10345595)
  - [HTTP 請求/回應格式](https://ithelp.ithome.com.tw/articles/10345737)
  - [實驗：使用 flask 與 telnet 實作 API](https://ithelp.ithome.com.tw/articles/10345871)
### 第四部分 AWS 服務
[<img src='https://ithelp.ithome.com.tw/upload/images/20240808/20129510u6xSlclLMa.png' width='5%'></img>](#%E5%9C%A8-aws-%E4%B8%8A%E9%80%B2%E8%A1%8C%E7%89%A9%E8%81%AF%E7%B6%B2%E8%88%87%E4%BA%BA%E5%B7%A5%E6%99%BA%E6%85%A7%E5%AF%A6%E4%BD%9C) [<img src='https://ithelp.ithome.com.tw/upload/images/20240808/201295100ApjQbzYXJ.png' width='5%'></img>](#bottom)
)
介紹本次應用中使用到的 AWS 的服務，包含了 API 呼叫、運算服務、儲存、資料庫與影像處理的人工智慧(AI)應用等。
  * [AWS 雲端基礎](https://ithelp.ithome.com.tw/articles/10346073)
  * [AWS 雲端安全](https://ithelp.ithome.com.tw/articles/10346204)
  * [申請 AWS 帳戶](https://ithelp.ithome.com.tw/articles/10346303)
  * [Amazon S3](https://ithelp.ithome.com.tw/articles/10346476)
  * [實驗：建立靜態網站](https://ithelp.ithome.com.tw/articles/10346625)
  * [Amazon API Gateway](https://ithelp.ithome.com.tw/articles/10346864)
  * [實驗：建立 API Gateway-using mock](https://ithelp.ithome.com.tw/articles/10346936)
  * [AWS Lambda](https://ithelp.ithome.com.tw/articles/10346986)
  * [實驗：使用 GET 方法查詢資料](https://ithelp.ithome.com.tw/articles/10347261)
  * [實驗：使用 POST 方法上傳圖片](https://ithelp.ithome.com.tw/articles/10347402)
  * [Amazon DynamoDB](https://ithelp.ithome.com.tw/articles/10347619)
  * [實驗：讀取 EXCEL 檔並存入資料庫中](https://ithelp.ithome.com.tw/articles/10347796)
  * [實驗：查詢資料庫中的資料](https://ithelp.ithome.com.tw/articles/10347980)
  * [Amazon Rekognition](https://ithelp.ithome.com.tw/articles/10348189)
  * [實驗：人臉辨識從 Amazon S3 讀取](https://ithelp.ithome.com.tw/articles/10348191)
  * [實驗：文字辨識從 Amazon S3 讀取](https://ithelp.ithome.com.tw/articles/10348192)
### 第五部分 系統整合
[<img src='https://ithelp.ithome.com.tw/upload/images/20240808/20129510u6xSlclLMa.png' width='5%'></img>](#%E5%9C%A8-aws-%E4%B8%8A%E9%80%B2%E8%A1%8C%E7%89%A9%E8%81%AF%E7%B6%B2%E8%88%87%E4%BA%BA%E5%B7%A5%E6%99%BA%E6%85%A7%E5%AF%A6%E4%BD%9C) [<img src='https://ithelp.ithome.com.tw/upload/images/20240808/201295100ApjQbzYXJ.png' width='5%'></img>](#bottom)

透過 API Gateway 整合 ESP32-CAM 與 AWS 服務，並透過網頁觀看結果。
  - [整合實驗：車牌辨識-定義功能](https://ithelp.ithome.com.tw/articles/10348193)
  - [實驗：後端 - API Gateway 上傳圖片並使用 POSTMAN 檢驗結果](https://ithelp.ithome.com.tw/articles/10352664)
  - [實驗：前端 - 使用 ESP32-CAM 呼叫 REST API 上傳圖片](https://ithelp.ithome.com.tw/articles/10352701)
  - [實驗：後端 - API Gateway 設定車牌辨識選項](https://ithelp.ithome.com.tw/articles/10353347)
  - [實驗：後端 - 觸動 S3 事件進行文字辨識](https://ithelp.ithome.com.tw/articles/10353398)
  - [實驗：後端 - API Gateway 查詢辨識記錄](https://ithelp.ithome.com.tw/articles/10353496)
  - [實驗：前端 - 使用 Web 用戶端 呼叫 REST API](https://ithelp.ithome.com.tw/articles/10353725)

相關程式碼已經上傳到 github，可以到[這裡](https://github.com/yehchitsai/AIoTnAWSCloud)下載

<a id='bottom'></a>

