// 加密 API 密钥
function encryptApiKey() {
    const apiKey = "a2c903cc-b31e-4547-9299-b6d07b7631ab";
    const apiKeyArray = apiKey.split("");
    const firstPart = apiKeyArray.splice(0, 8);
    // 将 API 密钥的前八位移至末尾
    return apiKeyArray.concat(firstPart).join("");
}

// 基于当前时间生成加密字符串
function encryptTime(currentTime) {
    const baseNumber = 1111111111111;
    const timeString = (currentTime + baseNumber).toString().split("");
    const randomSuffix = [
        parseInt(10 * Math.random(), 10),
        parseInt(10 * Math.random(), 10),
        parseInt(10 * Math.random(), 10)
    ];
    // 将随机生成的三个数添加到时间字符串末尾
    return timeString.concat(randomSuffix).join("");
}

// 将两个字符串组合并进行 Base64 编码
function combineAndEncode(firstString, secondString) {
    const combinedString = `${firstString}|${secondString}`;
    return Buffer.from(combinedString).toString('base64');
}

// 获取加密后的 API 密钥和时间的组合
function getApiKey() {
    const currentTime = new Date().getTime();
    const encryptedApiKey = encryptApiKey();
    const encryptedTime = encryptTime(currentTime);
    return combineAndEncode(encryptedApiKey, encryptedTime);
}
