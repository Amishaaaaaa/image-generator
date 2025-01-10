import React, { useState } from 'react';
import '../styles/WorkflowForm.css';

const WorkflowForm = ({ onGenerate }) => {
    const [seed, setSeed] = useState("");
    const [width, setWidth] = useState(512);
    const [height, setHeight] = useState(512);
    const [text, setText] = useState("beautiful scenery nature glass bottle landscape");

    const handleSubmit = (e) => {
        e.preventDefault();
        const params = {
            seed: seed || Math.floor(Math.random() * 1e9),
            width,
            height,
            text,
        };
        onGenerate(params);
    };

    return (
        <form onSubmit={handleSubmit}>
            <label>Seed:</label>
            <input type="number" value={seed} onChange={(e) => setSeed(e.target.value)} />

            <label>Width:</label>
            <input type="number" value={width} onChange={(e) => setWidth(e.target.value)} />

            <label>Height:</label>
            <input type="number" value={height} onChange={(e) => setHeight(e.target.value)} />

            <label>Prompt:</label>
            <textarea value={text} onChange={(e) => setText(e.target.value)} />

            <button type="submit">Generate</button>
        </form>
    );
};

export default WorkflowForm;
