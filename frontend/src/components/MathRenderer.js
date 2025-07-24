import React from 'react';
import { InlineMath, BlockMath } from 'react-katex';
import 'katex/dist/katex.min.css';

/**
 * MathRenderer component for displaying LaTeX math expressions
 * Supports both inline and block math rendering
 */
const MathRenderer = ({ children, block = false, className = '' }) => {
  if (!children) return null;
  
  // Clean up the LaTeX string
  const cleanMath = children
    .replace(/^\\\[|\\\]$/g, '') // Remove outer \[ \]
    .replace(/^\\\(|\\\)$/g, '') // Remove outer \( \)
    .trim();
  
  try {
    return block ? (
      <div className={`math-block ${className}`}>
        <BlockMath math={cleanMath} />
      </div>
    ) : (
      <span className={`math-inline ${className}`}>
        <InlineMath math={cleanMath} />
      </span>
    );
  } catch (error) {
    console.error('Math rendering error:', error);
    return (
      <span 
        style={{ 
          color: 'red', 
          backgroundColor: '#ffebee', 
          padding: '2px 4px', 
          borderRadius: '3px',
          fontSize: '0.9em'
        }}
      >
        Math Error: {children}
      </span>
    );
  }
};

/**
 * MathText component for rendering mixed text and math content
 * Automatically detects and renders LaTeX expressions in text
 */
export const MathText = ({ children, className = '' }) => {
  if (!children || typeof children !== 'string') {
    return <span className={className}>{children}</span>;
  }

  // Regular expressions to match LaTeX math expressions
  const blockMathRegex = /\\\[(.*?)\\\]/gs;
  const inlineMathRegex = /\\\((.*?)\\\)/gs;
  
  // Split text by math expressions while preserving the expressions
  const parts = children.split(/(\\$.*?\\$|\\\[.*?\\\]|\\\(.*?\\\))/gs);
  
  return (
    <span className={`math-text ${className}`}>
      {parts.map((part, index) => {
        // Check if this part is a math expression
        if (part.match(blockMathRegex)) {
          return <MathRenderer key={index} block>{part}</MathRenderer>;
        } else if (part.match(inlineMathRegex)) {
          return <MathRenderer key={index}>{part}</MathRenderer>;
        } else {
          // Regular text - preserve line breaks
          return part.split('\n').map((line, lineIndex, array) => (
            <React.Fragment key={`${index}-${lineIndex}`}>
              {line}
              {lineIndex < array.length - 1 && <br />}
            </React.Fragment>
          ));
        }
      })}
    </span>
  );
};

export default MathRenderer;
