const knownColors = {
  "Node.js": "#3c873a",
  "React": "#61dafb",
  "React Native": "#076d8a",
  "TypeScript": "#e948e9",
  "Python": "#551d9e",
  "Go": "#ecde5a",
  "Vue.js": "#41b883",
  "Java": "#b07219",
  "Docker": "#0273c9",
  "PostgreSQL": "#071968",
  "MongoDB": "#11380c",
  "Redis": "#d82c20",
  "AWS S3": "#ff9900",
};

const palette = [
  "#6366f1", "#8b5cf6", "#ec4899", "#f43f5e", "#f97316",
  "#eab308", "#22c55e", "#14b8a6", "#06b6d4", "#0ea5e9",
  "#a855f7", "#d946ef", "#e11d48", "#ca8a04", "#059669",
];

function hashString(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = str.charCodeAt(i) + ((hash << 5) - hash);
  }
  return Math.abs(hash);
}

function getColor(tech) {
  if (knownColors[tech]) return knownColors[tech];
  return palette[hashString(tech) % palette.length];
}

export function techBadgeStyle(tech) {
  const color = getColor(tech);
  return {
    background: `${color}18`,
    color: color,
    borderColor: `${color}44`,
  };
}
