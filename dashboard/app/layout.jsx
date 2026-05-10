import "./globals.css";

export const metadata = {
  title: "UK Spring Statement Analysis",
  description: "PolicyEngine analysis of Spring Statement household and fiscal impacts",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
