---
title: "Canvas"
description: "FalkorDB Canvas – a standalone web component for visualizing FalkorDB graphs using force-directed layouts."
parent: "Browser"
nav_order: 2
---

# FalkorDB Canvas

[FalkorDB Canvas](https://github.com/FalkorDB/falkordb-canvas) is a standalone web component for visualizing FalkorDB graphs using force-directed layouts. It is published as an npm package at [@falkordb/canvas](https://www.npmjs.com/package/@falkordb/canvas) and powers the graph visualization in FalkorDB Browser.

---

## Features

- **Force-directed graph layout** – Automatic positioning using D3 force simulation with smart collision detection
- **Multiple layout modes** – Switch between `force`, `tree`, and `radial` graph views
- **Interactive** – Click, hover, and right-click interactions on nodes, links, and background
- **Theme support** – Light and dark mode with customizable colors
- **Performance** – Optimized rendering with HTML5 Canvas, including viewport culling and low-zoom draw skipping for large graphs
- **Loading states** – Built-in skeleton loading with pulse animation
- **Customizable** – Colors, sizes, behaviors, and custom rendering functions
- **TypeScript support** – Full type definitions included
- **Web Component** – Works with any framework or vanilla JavaScript
- **Viewport control** – Zoom, pan, and auto-fit functionality

---

## Installation

```bash
npm install @falkordb/canvas
```

---

## Quick Start

### Vanilla JavaScript

```html
<!DOCTYPE html>
<html>
<head>
  <title>FalkorDB Canvas Example</title>
</head>
<body>
  <falkordb-canvas id="graph" style="width: 100%; height: 600px;"></falkordb-canvas>
  
  <script type="module">
    import '@falkordb/canvas';
    
    const canvas = document.getElementById('graph');
    
    // Set data
    canvas.setData({
      nodes: [
        { id: 1, labels: ['Person'], color: '#FF6B6B', visible: true, data: { name: 'Alice' } },
        { id: 2, labels: ['Person'], color: '#4ECDC4', visible: true, data: { name: 'Bob' } }
      ],
      links: [
        { id: 1, relationship: 'KNOWS', color: '#999', source: 1, target: 2, visible: true, data: {} }
      ]
    });
    
    // Configure
    canvas.setConfig({
      width: 800,
      height: 600,
      backgroundColor: '#FFFFFF',
      foregroundColor: '#1A1A1A',
      eventHandlers: {
        onNodeClick: (node) => console.log('Clicked:', node),
      },
    });
  </script>
</body>
</html>
```

### React / TypeScript

```tsx
import { useEffect, useRef } from 'react';
import '@falkordb/canvas';
import type { FalkorDBCanvas, Data, GraphNode } from '@falkordb/canvas';

function GraphVisualization() {
  const canvasRef = useRef<FalkorDBCanvas>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const data: Data = {
      nodes: [
        { id: 1, labels: ['Person'], color: '#FF6B6B', visible: true, data: { name: 'Alice' } },
        { id: 2, labels: ['Person'], color: '#4ECDC4', visible: true, data: { name: 'Bob' } }
      ],
      links: [
        { id: 1, relationship: 'KNOWS', color: '#999', source: 1, target: 2, visible: true, data: {} }
      ]
    };

    canvas.setData(data);
    canvas.setConfig({
      eventHandlers: {
        onNodeClick: (node: GraphNode) => {
          console.log('Clicked node:', node);
        },
      },
    });
  }, []);

  return (
    <falkordb-canvas 
      ref={canvasRef}
      style={{ width: '100%', height: '600px' }}
    />
  );
}
```

---

## API

### Methods

| Method | Description |
| :--- | :--- |
| `setData(data)` | Set the graph data (nodes and links). Automatically triggers layout simulation and loading states. |
| `getData()` | Get the current graph data in the simplified format. |
| `setGraphData(data)` | Set graph data in the internal format (with computed properties). Use for better performance when you already have `GraphData` format. |
| `getGraphData()` | Get the current graph data in the internal format with all computed properties. |
| `setConfig(config)` | Configure the graph visualization and behavior. Accepts a `ForceGraphConfig` object. |
| `setWidth(width)` | Set canvas width in pixels. |
| `setHeight(height)` | Set canvas height in pixels. |
| `setBackgroundColor(color)` | Set background color (hex or CSS color). |
| `setForegroundColor(color)` | Set foreground color for text and borders. |
| `setAnimation(enabled)` | Enable or disable force simulation animation. When disabled, pins all nodes in place. |
| `setPinOnDragEnd(pin)` | Enable or disable pinning nodes after dragging. |
| `setLayout(layoutMode)` | Switch layout mode: `'force'`, `'tree'`, or `'radial'`. |
| `setLayoutOptions(options)` | Update per-layout options (tree, radial, force). Triggers re-layout. |
| `setDebug(enabled)` | Enable or disable debug logging to console. |
| `refresh()` | Trigger a repaint after in-place property mutations (visibility, color, size). |
| `getViewport()` | Get current zoom and center position as `ViewportState`. |
| `setViewport(viewport)` | Restore a previously saved viewport state. |
| `getZoom()` | Get current zoom level. |
| `zoom(zoomLevel)` | Set zoom level. |
| `zoomToFit(paddingMultiplier, filter)` | Auto-fit all visible nodes in view. Optional padding multiplier and node filter function. |
| `getGraph()` | Get the underlying force-graph instance for advanced control. |
| `getCullingStats()` | Get viewport culling statistics (bounds, visible vs total node/link counts). |

---

### Configuration Options

Configuration is passed to `setConfig()` as a `ForceGraphConfig` object.

#### Top-Level Options

| Option | Default | Description |
| :--- | :--- | :--- |
| `width` | window width | Canvas width in pixels |
| `height` | window height | Canvas height in pixels |
| `backgroundColor` | `'#FFFFFF'` | Background color |
| `foregroundColor` | `'#1A1A1A'` | Foreground color for borders and text |
| `layoutMode` | `'force'` | Layout algorithm: `'force'`, `'tree'`, or `'radial'` |
| `layoutOptions` | `{}` | Per-layout options (see [Layout Modes](#layout-modes)) |
| `animation` | | Enable or disable layout animation |
| `captionsKeys` | `[]` | Node property keys to display as labels |
| `showPropertyKeyPrefix` | `false` | Show property key prefix in node labels |
| `pinOnDragEnd` | `false` | Pin nodes after dragging |
| `isNodeSelected` | | Function: `(node: GraphNode) => boolean` |
| `isLinkSelected` | | Function: `(link: GraphLink) => boolean` |
| `linkLineDash` | | Function: `(link: GraphLink) => number[]` |
| `node` | | Custom node rendering (see [Custom Rendering](#custom-rendering)) |
| `link` | | Custom link rendering (see [Custom Rendering](#custom-rendering)) |
| `largeGraph` | | Large-graph optimizations (see [Large-Graph Optimizations](#large-graph-optimizations)) |

#### Event Handlers

| Option | Description |
| :--- | :--- |
| `onNodeClick` | `(node: GraphNode, event: MouseEvent) => void` |
| `onNodeRightClick` | `(node: GraphNode, event: MouseEvent) => void` |
| `onLinkClick` | `(link: GraphLink, event: MouseEvent) => void` |
| `onLinkRightClick` | `(link: GraphLink, event: MouseEvent) => void` |
| `onNodeHover` | `(node: GraphNode \| null) => void` |
| `onNodeDragEnd` | `(node: GraphNode) => void` |
| `onPinChange` | `(pinned: boolean) => void` |
| `onLinkHover` | `(link: GraphLink \| null) => void` |
| `onBackgroundClick` | `(event: MouseEvent) => void` |
| `onBackgroundRightClick` | `(event: MouseEvent) => void` |
| `onZoom` | `(transform: Transform) => void` |
| `onEngineStop` | `() => void` |
| `onLayoutChange` | `(layout: LayoutMode) => void` |

---

### Layout Modes

Use `layoutMode` in `setConfig` to choose the graph view style:

#### Force (default)

The default physics-based layout using D3 force simulation with configurable physics parameters.

#### Tree

```typescript
canvas.setConfig({
  layoutMode: 'tree',
  layoutOptions: {
    tree: {
      direction: 'lr',      // 'lr' | 'rl' | 'td' | 'bu'
      levelDistance: 180,
      nodeSpacing: 110
    }
  }
});
```

#### Radial

```typescript
canvas.setConfig({
  layoutMode: 'radial',
  layoutOptions: {
    radial: {
      direction: 'out',   // 'out' | 'in'
      levelDistance: 130
    }
  }
});
```

---

### Data Types

#### Node

| Property | Default | Description |
| :--- | :--- | :--- |
| `id` | *required* | Unique identifier for the node |
| `labels` | *required* | Array of label names for the node |
| `color` | *required* | Node color (hex or CSS color) |
| `visible` | *required* | Whether the node is visible |
| `size` | `9` | Node radius (world units) |
| `caption` | `'id'` | Property key to use from the data for display text |
| `data` | *required* | Node properties as key-value pairs |

#### Link

| Property | Default | Description |
| :--- | :--- | :--- |
| `id` | *required* | Unique identifier for the link |
| `relationship` | *required* | Label displayed on the link |
| `color` | *required* | Link color (hex or CSS color) |
| `source` | *required* | Source node ID |
| `target` | *required* | Target node ID |
| `visible` | *required* | Whether the link is visible |
| `data` | *required* | Link properties as key-value pairs |

---

## Custom Rendering

You can provide custom rendering functions for nodes and links:

```typescript
canvas.setConfig({
  node: {
    nodeCanvasObject: (node: GraphNode, ctx: CanvasRenderingContext2D) => {
      // Custom node drawing logic
      ctx.fillStyle = node.color;
      ctx.fillRect(node.x! - 5, node.y! - 5, 10, 10);
    },
    nodePointerAreaPaint: (node: GraphNode, color: string, ctx: CanvasRenderingContext2D) => {
      // Define clickable area
      ctx.fillStyle = color;
      ctx.fillRect(node.x! - 5, node.y! - 5, 10, 10);
    }
  },
  link: {
    linkCanvasObject: (link: GraphLink, ctx: CanvasRenderingContext2D) => {
      // Custom link drawing logic
    },
    linkPointerAreaPaint: (link: GraphLink, color: string, ctx: CanvasRenderingContext2D) => {
      // Define clickable area for link
    }
  }
});
```

The `node-mode` and `link-mode` HTML attributes control how custom rendering combines with default rendering:

```html
<falkordb-canvas 
  node-mode="replace"
  link-mode="after">
</falkordb-canvas>
```

- `replace` (default for nodes) – Uses custom rendering exclusively
- `before` – Renders custom content before default rendering
- `after` (default for links) – Renders custom content after default rendering

---

## Large-Graph Optimizations

For graphs with thousands of nodes and links, enable viewport culling and low-zoom draw skipping:

```typescript
canvas.setConfig({
  largeGraph: {
    enabled: true,
    viewportPadding: 100,
    lowZoomThreshold: 0.4,
    skipLabelsAtLowZoom: true,
    skipArrowsAtLowZoom: true,
    skipLinkLabelsAtLowZoom: true,
  }
});
```

| Option | Default | Description |
| :--- | :--- | :--- |
| `enabled` | `true` | Master switch for large-graph optimizations |
| `viewportPadding` | `0` | World-unit padding around the visible viewport |
| `lowZoomThreshold` | `1` | Zoom level below which expensive details are skipped |
| `skipLabelsAtLowZoom` | `true` | Skip node labels at low zoom |
| `skipArrowsAtLowZoom` | `true` | Skip link arrowheads at low zoom |
| `skipLinkLabelsAtLowZoom` | `true` | Skip link relationship labels at low zoom |

---

## Utility Functions

The package exports utility functions for data manipulation:

```typescript
import {
  dataToGraphData,
  graphDataToData,
  getNodeDisplayText,
  getNodeDisplayKey,
  wrapTextForCircularNode
} from '@falkordb/canvas';

// Convert between formats
const graphData = dataToGraphData(data);
const simpleData = graphDataToData(graphData);

// Get display text for a node
const text = getNodeDisplayText(node);

// Wrap text for circular nodes
const [line1, line2] = wrapTextForCircularNode(ctx, text, radius);
```

---

## Performance Tips

1. **Large graphs** – Disable animation (`setAnimation(false)`) once the layout stabilizes
2. **Static graphs** – Use a deterministic layout (`setLayout('tree')`) to avoid simulation overhead
3. **Custom rendering** – Optimize your custom `nodeCanvasObject` and `linkCanvasObject` functions
4. **Viewport** – Use `getViewport()` and `setViewport()` to preserve the user's view when updating data
5. **Very large graphs** – Enable viewport culling via the `largeGraph` option

---

## Browser Support

- Chrome / Edge (latest)
- Firefox (latest)
- Safari (latest)

Requires support for Web Components (Custom Elements), ES Modules, Shadow DOM, and HTML5 Canvas.

---

## Links

- [GitHub Repository](https://github.com/FalkorDB/falkordb-canvas)
- [npm Package](https://www.npmjs.com/package/@falkordb/canvas)
