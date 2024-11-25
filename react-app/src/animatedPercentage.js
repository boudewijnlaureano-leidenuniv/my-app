import React, { useState, useEffect } from 'react';
import { NodeGroup } from 'react-move';

const AnimatedPercentage = ({ maxPercentage = 100, animationDuration = 1000, barColor = '#e76224' }) => {
  const [percentage, setPercentage] = useState(0);

  useEffect(() => {
    if (percentage < maxPercentage) {
      const interval = setInterval(() => {
        setPercentage((prev) => Math.min(prev + 1, maxPercentage));
      }, animationDuration / maxPercentage);

      return () => clearInterval(interval);
    }
  }, [percentage, maxPercentage, animationDuration]);

  return (
    <NodeGroup
      data={[{ id: 1, value: percentage }]}
      keyAccessor={(d) => d.id}
      start={() => ({
        opacity: 0,
        translateY: 30,
      })}
      enter={() => ({
        opacity: [1],
        translateY: [0],
        timing: { duration: animationDuration / maxPercentage },
      })}
      update={() => ({
        opacity: [1],
        translateY: [0],
        timing: { duration: animationDuration / maxPercentage },
      })}
    >
      {(nodes) => (
        <div style={{ display: 'flex', overflow: 'hidden' }}>
          {nodes.map(({ key, data, state: { opacity, translateY } }) => (
            <span
              key={key}
              style={{
                opacity,
                transform: `translateY(${translateY}px)`,
                display: 'inline-block',
                fontSize: '2em',
              }}
            >
              {`${data.value}%`}
            </span>
          ))}
        </div>
      )}
    </NodeGroup>
  );
};

export default AnimatedPercentage;
