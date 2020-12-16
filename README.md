# **109final**

> python實作 期末專題

模型用法：

先使用train_test.py，他會進train資料夾，抓取裡面的圖片跟檔名。

可以修改程式碼中的epoch修改訓練次數，目前預設是10次。

執行完後得到.h5結尾的檔案後，可以執行predict.py。

輸入需預測的圖片檔名（副檔名也要輸入）例如：testing/01.png

就可以預測了。

---

### 增加準確度方法：

1. 執行get_img.py，他會從tronclass上面測試現有模型，正確的就把圖片抓下來，放進robot_got_img資料夾中，錯誤的就放入wrong資料夾，同時會更改檔名變成他預測的。
2. 一次迴圈目前是100次，執行完後，可以將robot_got_img中的圖片放入traning資料夾，並從woring資料夾中複製一份辨識錯誤的圖片，人工將檔名修改成正確之後，一併丟到train資料夾。
3. 重新執行train_test.py
4. 使用predict.py確認是否能正確辨識之前錯的。

