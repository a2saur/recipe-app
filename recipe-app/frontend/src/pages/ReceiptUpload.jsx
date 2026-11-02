import { useState } from "react";
import { processReceiptHTML } from "../utils/processReceiptHTML";

export default function ReceiptUpload({ onSave }){
    const [content, setContent] = useState("");
    const [preview, setPreview] = useState("");
    // const receiptItems;

    function handleContentChange(event){
        let newContent = "";
        event.target.value.split("\n").map((line, index) => {
            if (line.replaceAll("\t", "").replaceAll(" ", "") !== "") { 
                newContent += line;
                newContent += "\n";
            }
        });

        setContent(newContent);

        // processHTML(newContent).map((info) => 
        //     preview += 
        // )
        setPreview(processReceiptHTML(newContent));
    }

    function handleSubmit(event){
        
    }

    return (
        <main>
            {preview}
            Hi
            <form className="receipt-upload">
                <textarea id="html-content" 
                        rows="100" cols="100"
                        value={content}
                        onChange={handleContentChange}
                        ></textarea>
            </form>
        </main>
    )
}