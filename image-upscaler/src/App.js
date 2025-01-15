import React, { useState } from "react";
import axios from "axios";

function App() {
  const [lowResImage, setLowResImage] = useState(null);
  const [highResImage, setHighResImage] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setLowResImage(URL.createObjectURL(file)); // Display the low-res image locally.

      const formData = new FormData();
      formData.append("image", file);

      setLoading(true); // Show loading while processing the image.

      // Send the image to the backend for upscaling
      axios
        .post("http://127.0.0.1:5000/upscale", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
          responseType: "blob", // Expect binary data (image) in response
        })
        .then((response) => {
          const highResBlob = new Blob([response.data], { type: "image/jpeg" });
          setHighResImage(URL.createObjectURL(highResBlob)); // Display high-res image
          setLoading(false);
        })
        .catch((error) => {
          console.error("Error processing the image:", error);
          setLoading(false);
        });
    }
  };

  const downloadHighResImage = () => {
    const link = document.createElement("a");
    link.href = highResImage;
    link.download = "high_res_image.jpg";
    link.click();
  };

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h1>Image Upscaler</h1>
      <input
        type="file"
        accept="image/*"
        onChange={handleFileUpload}
        style={{ margin: "20px 0" }}
      />
      {loading && <p>Processing your image...</p>}
      <div style={{ display: "flex", justifyContent: "center", gap: "20px", marginTop: "20px" }}>
        {lowResImage && (
          <div>
            <h3>Low-Resolution Image</h3>
            <img
              src={lowResImage}
              alt="Low Resolution"
              style={{ width: "300px", border: "1px solid #ccc" }}
            />
          </div>
        )}
        {highResImage && (
          <div>
            <h3>High-Resolution Image</h3>
            <img
              src={highResImage}
              alt="High Resolution"
              style={{ width: "300px", border: "1px solid #ccc" }}
            />
            <button
              onClick={downloadHighResImage}
              style={{ marginTop: "10px", padding: "10px 20px" }}
            >
              Download High-Res Image
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
