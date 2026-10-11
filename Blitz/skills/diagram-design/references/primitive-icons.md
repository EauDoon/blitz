# Icons (primitive)

A monochrome 24×24 icon library for IT/cloud diagrams. Each icon uses `currentColor` so it inherits ink from its parent SVG and adapts to the editorial skin or any user-onboarded brand palette.

## Usage

Find the icon by name (the `### name` headings below). Copy the fenced `<svg>` snippet into your diagram. Default size is 24×24; wrap in `<g transform="translate(x,y) scale(s)">` to position and resize. Set `color`, `fill`, or `stroke` on the parent group/SVG to control color.

All graphics are stroked. The 50 generic Tabler icons retain their MIT notice. The 37 product-specific keys use newly authored generic stand-ins, not official brand artwork. Several products deliberately share a functional symbol; distinguish them with text labels. Product lookup keys and semantic node labels are preserved, but official brand recognition is no longer a feature of this collection.

## Compute

### laptop
User laptop or workstation.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 19l18 0" /> <path d="M5 7a1 1 0 0 1 1 -1h12a1 1 0 0 1 1 1v8a1 1 0 0 1 -1 1h-12a1 1 0 0 1 -1 -1l0 -8" /></svg>
```

Source: Tabler Icons / `device-laptop` (MIT)

### phone
Mobile phone or tablet client.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M6 5a2 2 0 0 1 2 -2h8a2 2 0 0 1 2 2v14a2 2 0 0 1 -2 2h-8a2 2 0 0 1 -2 -2v-14" /> <path d="M11 4h2" /> <path d="M12 17v.01" /></svg>
```

Source: Tabler Icons / `device-mobile` (MIT)

### desktop
Desktop computer.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 5a1 1 0 0 1 1 -1h16a1 1 0 0 1 1 1v10a1 1 0 0 1 -1 1h-16a1 1 0 0 1 -1 -1v-10" /> <path d="M7 20h10" /> <path d="M9 16v4" /> <path d="M15 16v4" /></svg>
```

Source: Tabler Icons / `device-desktop` (MIT)

### server
Physical server or VM host.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 7a3 3 0 0 1 3 -3h12a3 3 0 0 1 3 3v2a3 3 0 0 1 -3 3h-12a3 3 0 0 1 -3 -3" /> <path d="M3 15a3 3 0 0 1 3 -3h12a3 3 0 0 1 3 3v2a3 3 0 0 1 -3 3h-12a3 3 0 0 1 -3 -3l0 -2" /> <path d="M7 8l0 .01" /> <path d="M7 16l0 .01" /></svg>
```

Source: Tabler Icons / `server` (MIT)

### container
Container image or running instance.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l8 4.5l0 9l-8 4.5l-8 -4.5l0 -9l8 -4.5" /> <path d="M12 12l8 -4.5" /> <path d="M12 12l0 9" /> <path d="M12 12l-8 -4.5" /> <path d="M16 5.25l-8 4.5" /></svg>
```

Source: Tabler Icons / `package` (MIT)

### vm
Virtual machine.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16.008v-8.018a1.98 1.98 0 0 0 -1 -1.717l-7 -4.008a2.016 2.016 0 0 0 -2 0l-7 4.008c-.619 .355 -1 1.01 -1 1.718v8.018c0 .709 .381 1.363 1 1.717l7 4.008a2.016 2.016 0 0 0 2 0l7 -4.008c.619 -.355 1 -1.01 1 -1.718" /> <path d="M12 22v-10" /> <path d="M12 12l8.73 -5.04" /> <path d="M3.27 6.96l8.73 5.04" /></svg>
```

Source: Tabler Icons / `cube` (MIT)

## People

### user
End user or single actor.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M8 7a4 4 0 1 0 8 0a4 4 0 0 0 -8 0" /> <path d="M6 21v-2a4 4 0 0 1 4 -4h4a4 4 0 0 1 4 4v2" /></svg>
```

Source: Tabler Icons / `user` (MIT)

### users
Group / cohort / team.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 7a4 4 0 1 0 8 0a4 4 0 1 0 -8 0" /> <path d="M3 21v-2a4 4 0 0 1 4 -4h4a4 4 0 0 1 4 4v2" /> <path d="M16 3.13a4 4 0 0 1 0 7.75" /> <path d="M21 21v-2a4 4 0 0 0 -3 -3.85" /></svg>
```

Source: Tabler Icons / `users` (MIT)

### admin
Privileged user / admin.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M6 21v-2a4 4 0 0 1 4 -4h2" /> <path d="M22 16c0 4 -2.5 6 -3.5 6s-3.5 -2 -3.5 -6c1 0 2.5 -.5 3.5 -1.5c1 1 2.5 1.5 3.5 1.5" /> <path d="M8 7a4 4 0 1 0 8 0a4 4 0 0 0 -8 0" /></svg>
```

Source: Tabler Icons / `user-shield` (MIT)

### robot
Bot, agent, or automated process.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M6 6a2 2 0 0 1 2 -2h8a2 2 0 0 1 2 2v4a2 2 0 0 1 -2 2h-8a2 2 0 0 1 -2 -2l0 -4" /> <path d="M12 2v2" /> <path d="M9 12v9" /> <path d="M15 12v9" /> <path d="M5 16l4 -2" /> <path d="M15 14l4 2" /> <path d="M9 18h6" /> <path d="M10 8v.01" /> <path d="M14 8v.01" /></svg>
```

Source: Tabler Icons / `robot` (MIT)

## Network

### cloud
Cloud provider or boundary.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M6.657 18c-2.572 0 -4.657 -2.007 -4.657 -4.483c0 -2.475 2.085 -4.482 4.657 -4.482c.393 -1.762 1.794 -3.2 3.675 -3.773c1.88 -.572 3.956 -.193 5.444 1c1.488 1.19 2.162 3.007 1.77 4.769h.99c1.913 0 3.464 1.56 3.464 3.486c0 1.927 -1.551 3.487 -3.465 3.487h-11.878" /></svg>
```

Source: Tabler Icons / `cloud` (MIT)

### internet
Public internet.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 1 0 18 0a9 9 0 0 0 -18 0" /> <path d="M3.6 9h16.8" /> <path d="M3.6 15h16.8" /> <path d="M11.5 3a17 17 0 0 0 0 18" /> <path d="M12.5 3a17 17 0 0 1 0 18" /></svg>
```

Source: Tabler Icons / `world` (MIT)

### cdn
CDN or edge cache.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M19.5 7a9 9 0 0 0 -7.5 -4a8.991 8.991 0 0 0 -7.484 4" /> <path d="M11.5 3a16.989 16.989 0 0 0 -1.826 4" /> <path d="M12.5 3a16.989 16.989 0 0 1 1.828 4" /> <path d="M19.5 17a9 9 0 0 1 -7.5 4a8.991 8.991 0 0 1 -7.484 -4" /> <path d="M11.5 21a16.989 16.989 0 0 1 -1.826 -4" /> <path d="M12.5 21a16.989 16.989 0 0 0 1.828 -4" /> <path d="M2 10l1 4l1.5 -4l1.5 4l1 -4" /> <path d="M17 10l1 4l1.5 -4l1.5 4l1 -4" /> <path d="M9.5 10l1 4l1.5 -4l1.5 4l1 -4" /></svg>
```

Source: Tabler Icons / `world-www` (MIT)

### firewall
Firewall or perimeter control.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6a2 2 0 0 1 2 -2h12a2 2 0 0 1 2 2v12a2 2 0 0 1 -2 2h-12a2 2 0 0 1 -2 -2l0 -12" /> <path d="M4 8h16" /> <path d="M20 12h-16" /> <path d="M4 16h16" /> <path d="M9 4v4" /> <path d="M14 8v4" /> <path d="M8 12v4" /> <path d="M16 12v4" /> <path d="M11 16v4" /></svg>
```

Source: Tabler Icons / `wall` (MIT)

### vpn
VPN or encrypted tunnel.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a12 12 0 0 0 8.5 3a12 12 0 0 1 -8.5 15a12 12 0 0 1 -8.5 -15a12 12 0 0 0 8.5 -3" /> <path d="M11 11a1 1 0 1 0 2 0a1 1 0 1 0 -2 0" /> <path d="M12 12l0 2.5" /></svg>
```

Source: Tabler Icons / `shield-lock` (MIT)

### load-balancer
Load balancer / traffic split.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 17h-8l-3.5 -5h-6.5" /> <path d="M21 7h-8l-3.495 5" /> <path d="M18 10l3 -3l-3 -3" /> <path d="M18 20l3 -3l-3 -3" /></svg>
```

Source: Tabler Icons / `arrows-split` (MIT)

### gateway
API gateway or ingress door.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M13 12v.01" /> <path d="M3 21h18" /> <path d="M5 21v-16a2 2 0 0 1 2 -2h6m4 10.5v7.5" /> <path d="M21 7h-7m3 -3l-3 3l3 3" /></svg>
```

Source: Tabler Icons / `door-enter` (MIT)

### dns
DNS / name resolution.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M6.5 7.5a1 1 0 1 0 2 0a1 1 0 1 0 -2 0" /> <path d="M3 6v5.172a2 2 0 0 0 .586 1.414l7.71 7.71a2.41 2.41 0 0 0 3.408 0l5.592 -5.592a2.41 2.41 0 0 0 0 -3.408l-7.71 -7.71a2 2 0 0 0 -1.414 -.586h-5.172a3 3 0 0 0 -3 3" /></svg>
```

Source: Tabler Icons / `tag` (MIT)

## Data

### database
Relational or document database.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6a8 3 0 1 0 16 0a8 3 0 1 0 -16 0" /> <path d="M4 6v6a8 3 0 0 0 16 0v-6" /> <path d="M4 12v6a8 3 0 0 0 16 0v-6" /></svg>
```

Source: Tabler Icons / `database` (MIT)

### file
Generic file.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14 3v4a1 1 0 0 0 1 1h4" /> <path d="M17 21h-10a2 2 0 0 1 -2 -2v-14a2 2 0 0 1 2 -2h7l5 5v11a2 2 0 0 1 -2 2" /></svg>
```

Source: Tabler Icons / `file` (MIT)

### log
Log file / event stream.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14 3v4a1 1 0 0 0 1 1h4" /> <path d="M17 21h-10a2 2 0 0 1 -2 -2v-14a2 2 0 0 1 2 -2h7l5 5v11a2 2 0 0 1 -2 2" /> <path d="M9 9l1 0" /> <path d="M9 13l6 0" /> <path d="M9 17l6 0" /></svg>
```

Source: Tabler Icons / `file-text` (MIT)

### queue
Message queue / FIFO.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4l-8 4l8 4l8 -4l-8 -4" /> <path d="M4 12l8 4l8 -4" /> <path d="M4 16l8 4l8 -4" /></svg>
```

Source: Tabler Icons / `stack-2` (MIT)

### cache
Cache layer.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M13 3l0 7l6 0l-8 11l0 -7l-6 0l8 -11" /></svg>
```

Source: Tabler Icons / `bolt` (MIT)

### bucket
Object storage / S3 bucket.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 7a8 4 0 1 0 16 0a8 4 0 1 0 -16 0" /> <path d="M4 7c0 .664 .088 1.324 .263 1.965l2.737 10.035c.5 1.5 2.239 2 5 2s4.5 -.5 5 -2c.333 -1 1.246 -4.345 2.737 -10.035a7.45 7.45 0 0 0 .263 -1.965" /></svg>
```

Source: Tabler Icons / `bucket` (MIT)

### backup
Backup or snapshot.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M6 4h10l4 4v10a2 2 0 0 1 -2 2h-12a2 2 0 0 1 -2 -2v-12a2 2 0 0 1 2 -2" /> <path d="M10 14a2 2 0 1 0 4 0a2 2 0 1 0 -4 0" /> <path d="M14 4l0 4l-6 0l0 -4" /></svg>
```

Source: Tabler Icons / `device-floppy` (MIT)

### search
Search index / query.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 10a7 7 0 1 0 14 0a7 7 0 1 0 -14 0" /> <path d="M21 21l-6 -6" /></svg>
```

Source: Tabler Icons / `search` (MIT)

## Kubernetes

### pod
Pod (smallest deployable unit).

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M19.875 6.27a2.225 2.225 0 0 1 1.125 1.948v7.284c0 .809 -.443 1.555 -1.158 1.948l-6.75 4.27a2.269 2.269 0 0 1 -2.184 0l-6.75 -4.27a2.225 2.225 0 0 1 -1.158 -1.948v-7.285c0 -.809 .443 -1.554 1.158 -1.947l6.75 -3.98a2.33 2.33 0 0 1 2.25 0l6.75 3.98h-.033" /></svg>
```

Source: Tabler Icons / `hexagon` (MIT)

### node
Cluster node.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M8 18a2 2 0 1 0 -4 0a2 2 0 0 0 4 0" /> <path d="M20 6a2 2 0 1 0 -4 0a2 2 0 0 0 4 0" /> <path d="M8 6a2 2 0 1 0 -4 0a2 2 0 0 0 4 0" /> <path d="M20 18a2 2 0 1 0 -4 0a2 2 0 0 0 4 0" /> <path d="M14 12a2 2 0 1 0 -4 0a2 2 0 0 0 4 0" /> <path d="M7.5 7.5l3 3" /> <path d="M7.5 16.5l3 -3" /> <path d="M13.5 13.5l3 3" /> <path d="M16.5 7.5l-3 3" /></svg>
```

Source: Tabler Icons / `topology-star` (MIT)

### service
K8s service / virtual endpoint.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 1 0 -8.979 9" /> <path d="M3.6 9h16.8" /> <path d="M3.6 15h8.9" /> <path d="M11.5 3a17 17 0 0 0 0 18" /> <path d="M12.5 3a16.992 16.992 0 0 1 2.522 10.376" /> <path d="M17.001 19a2 2 0 1 0 4 0a2 2 0 1 0 -4 0" /> <path d="M19.001 15.5v1.5" /> <path d="M19.001 21v1.5" /> <path d="M22.032 17.25l-1.299 .75" /> <path d="M17.27 20l-1.3 .75" /> <path d="M15.97 17.25l1.3 .75" /> <path d="M20.733 20l1.3 .75" /></svg>
```

Source: Tabler Icons / `world-cog` (MIT)

### deployment
Deployment rollout.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 13a8 8 0 0 1 7 7a6 6 0 0 0 3 -5a9 9 0 0 0 6 -8a3 3 0 0 0 -3 -3a9 9 0 0 0 -8 6a6 6 0 0 0 -5 3" /> <path d="M7 14a6 6 0 0 0 -3 6a6 6 0 0 0 6 -3" /> <path d="M14 9a1 1 0 1 0 2 0a1 1 0 1 0 -2 0" /></svg>
```

Source: Tabler Icons / `rocket` (MIT)

### ingress
Ingress controller / route in.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M8 12h13" /> <path d="M18 9l3 3l-3 3" /> <path d="M5.5 9.5l-2.5 2.5l2.5 2.5l2.5 -2.5l-2.5 -2.5" /></svg>
```

Source: Tabler Icons / `arrow-right-rhombus` (MIT)

### volume
Persistent volume.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M7 21h10a2 2 0 0 0 2 -2v-14a2 2 0 0 0 -2 -2h-6.172a2 2 0 0 0 -1.414 .586l-3.828 3.828a2 2 0 0 0 -.586 1.414v10.172a2 2 0 0 0 2 2" /> <path d="M13 6v2" /> <path d="M16 6v2" /> <path d="M10 7v1" /></svg>
```

Source: Tabler Icons / `device-sd-card` (MIT)

## Action

### api
API surface / endpoint.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M7 4a2 2 0 0 0 -2 2v3a2 3 0 0 1 -2 3a2 3 0 0 1 2 3v3a2 2 0 0 0 2 2" /> <path d="M17 4a2 2 0 0 1 2 2v3a2 3 0 0 0 2 3a2 3 0 0 0 -2 3v3a2 2 0 0 1 -2 2" /></svg>
```

Source: Tabler Icons / `braces` (MIT)

### request
Outbound request.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12l14 0" /> <path d="M13 18l6 -6" /> <path d="M13 6l6 6" /></svg>
```

Source: Tabler Icons / `arrow-right` (MIT)

### response
Inbound response.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12l14 0" /> <path d="M5 12l6 6" /> <path d="M5 12l6 -6" /></svg>
```

Source: Tabler Icons / `arrow-left` (MIT)

### sync
Sync / reconcile loop.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 11a8.1 8.1 0 0 0 -15.5 -2m-.5 -4v4h4" /> <path d="M4 13a8.1 8.1 0 0 0 15.5 2m.5 4v-4h-4" /></svg>
```

Source: Tabler Icons / `refresh` (MIT)

### lock
Locked / authenticated.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 13a2 2 0 0 1 2 -2h10a2 2 0 0 1 2 2v6a2 2 0 0 1 -2 2h-10a2 2 0 0 1 -2 -2v-6" /> <path d="M11 16a1 1 0 1 0 2 0a1 1 0 0 0 -2 0" /> <path d="M8 11v-4a4 4 0 1 1 8 0v4" /></svg>
```

Source: Tabler Icons / `lock` (MIT)

### key
Key / secret.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M16.555 3.843l3.602 3.602a2.877 2.877 0 0 1 0 4.069l-2.643 2.643a2.877 2.877 0 0 1 -4.069 0l-.301 -.301l-6.558 6.558a2 2 0 0 1 -1.239 .578l-.175 .008h-1.172a1 1 0 0 1 -.993 -.883l-.007 -.117v-1.172a2 2 0 0 1 .467 -1.284l.119 -.13l.414 -.414h2v-2h2v-2l2.144 -2.144l-.301 -.301a2.877 2.877 0 0 1 0 -4.069l2.643 -2.643a2.877 2.877 0 0 1 4.069 0" /> <path d="M15 9h.01" /></svg>
```

Source: Tabler Icons / `key` (MIT)

### alert
Warning / paged alert.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 9v4" /> <path d="M10.363 3.591l-8.106 13.534a1.914 1.914 0 0 0 1.636 2.871h16.214a1.914 1.914 0 0 0 1.636 -2.87l-8.106 -13.536a1.914 1.914 0 0 0 -3.274 0" /> <path d="M12 16h.01" /></svg>
```

Source: Tabler Icons / `alert-triangle` (MIT)

## DevOps

### git-branch
Branch / fork point.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 18a2 2 0 1 0 4 0a2 2 0 1 0 -4 0" /> <path d="M5 6a2 2 0 1 0 4 0a2 2 0 1 0 -4 0" /> <path d="M15 6a2 2 0 1 0 4 0a2 2 0 1 0 -4 0" /> <path d="M7 8l0 8" /> <path d="M9 18h6a2 2 0 0 0 2 -2v-5" /> <path d="M14 14l3 -3l3 3" /></svg>
```

Source: Tabler Icons / `git-branch` (MIT)

### terminal
Shell / CLI.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 7l5 5l-5 5" /> <path d="M12 19l7 0" /></svg>
```

Source: Tabler Icons / `terminal` (MIT)

### pipeline
CI/CD pipeline.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 18a2 2 0 1 0 4 0a2 2 0 1 0 -4 0" /> <path d="M5 6a2 2 0 1 0 4 0a2 2 0 1 0 -4 0" /> <path d="M15 12a2 2 0 1 0 4 0a2 2 0 1 0 -4 0" /> <path d="M7 8l0 8" /> <path d="M7 8a4 4 0 0 0 4 4h4" /></svg>
```

Source: Tabler Icons / `git-merge` (MIT)

### bug
Bug / defect.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 9v-1a3 3 0 0 1 6 0v1" /> <path d="M8 9h8a6 6 0 0 1 1 3v3a5 5 0 0 1 -10 0v-3a6 6 0 0 1 1 -3" /> <path d="M3 13l4 0" /> <path d="M17 13l4 0" /> <path d="M12 20l0 -6" /> <path d="M4 19l3.35 -2" /> <path d="M20 19l-3.35 -2" /> <path d="M4 7l3.75 2.4" /> <path d="M20 7l-3.75 2.4" /></svg>
```

Source: Tabler Icons / `bug` (MIT)

### monitoring
Metrics / observability.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19l16 0" /> <path d="M4 15l4 -6l4 2l4 -5l4 4" /></svg>
```

Source: Tabler Icons / `chart-line` (MIT)

### test
Test / experiment.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 8.04l-12.122 12.124a2.857 2.857 0 1 1 -4.041 -4.04l12.122 -12.124" /> <path d="M7 13h8" /> <path d="M19 15l1.5 1.6a2 2 0 1 1 -3 0l1.5 -1.6" /> <path d="M15 3l6 6" /></svg>
```

Source: Tabler Icons / `test-pipe` (MIT)

## Product nodes (generic symbols)

### docker
Docker engine / image. Uses a generic container service symbol, not an official product logo. Keep the product name as a separate text label.

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" role="img"><title>Generic container service symbol for docker; not an official logo</title><rect x="3" y="5" width="18" height="14" rx="1"/><rect x="6" y="9" width="4" height="6"/><rect x="14" y="9" width="4" height="6"/><path d="M10 12h4"/></svg>
```

Source: Newly authored basic SVG geometry for Blitz v2.1OAI, 11-10-2026. See `../THIRD_PARTY_LICENSES.md` for provenance and the complete replacement inventory.

### terraform
Terraform infrastructure as code. Uses a generic infrastructure plan symbol, not an official product logo. Keep the product name as a separate text label.

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" role="img"><title>Generic infrastructure plan symbol for terraform; not an official logo</title><rect x="3" y="3" width="18" height="18" rx="1"/><path d="M7 7h10M7 12h4v5h6M11 12h6M7 17h1"/></svg>
```

Source: Newly authored basic SVG geometry for Blitz v2.1OAI, 11-10-2026. See `../THIRD_PARTY_LICENSES.md` for provenance and the complete replacement inventory.

### aws
Amazon Web Services. Uses a generic cloud services symbol, not an official product logo. Keep the product name as a separate text label.

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" role="img"><title>Generic cloud services symbol for aws; not an official logo</title><rect x="3" y="3" width="18" height="18" rx="3"/><rect x="6" y="7" width="4" height="4"/><rect x="14" y="7" width="4" height="4"/><path d="M8 15h8M12 11v7"/></svg>
```

Source: Newly authored basic SVG geometry for Blitz v2.1OAI, 11-10-2026. See `../THIRD_PARTY_LICENSES.md` for provenance and the complete replacement inventory.

### azure
Microsoft Azure. Uses a generic cloud services symbol, not an official product logo. Keep the product name as a separate text label.

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" role="img"><title>Generic cloud services symbol for azure; not an official logo</title><rect x="3" y="3" width="18" height="18" rx="3"/><rect x="6" y="7" width="4" height="4"/><rect x="14" y="7" width="4" height="4"/><path d="M8 15h8M12 11v7"/></svg>
```

Source: Newly authored basic SVG geometry for Blitz v2.1OAI, 11-10-2026. See `../THIRD_PARTY_LICENSES.md` for provenance and the complete replacement inventory.

### github
GitHub. Uses a generic source repository symbol, not an official product logo. Keep the product name as a separate text label.

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" role="img"><title>Generic source repository symbol for github; not an official logo</title><rect x="3" y="3" width="18" height="18" rx="1"/><circle cx="8" cy="7" r="1.5"/><circle cx="8" cy="17" r="1.5"/><circle cx="16" cy="9" r="1.5"/><path d="M8 8.5v7M8 12h8v-1.5"/></svg>
```

Source: Newly authored basic SVG geometry for Blitz v2.1OAI, 11-10-2026. See `../THIRD_PARTY_LICENSES.md` for provenance and the complete replacement inventory.

### kubernetes
Kubernetes. Uses a generic service cluster symbol, not an official product logo. Keep the product name as a separate text label.

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" role="img"><title>Generic service cluster symbol for kubernetes; not an official logo</title><rect x="2" y="3" width="7" height="7" rx="1"/><rect x="15" y="3" width="7" height="7" rx="1"/><rect x="8.5" y="15" width="7" height="7" rx="1"/><path d="M5.5 10v2.5h13V10M12 12.5V15"/></svg>
```

Source: Newly authored basic SVG geometry for Blitz v2.1OAI, 11-10-2026. See `../THIRD_PARTY_LICENSES.md` for provenance and the complete replacement inventory.

### gcp
Google Cloud. Uses a generic cloud services symbol, not an official product logo. Keep the product name as a separate text label.

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" role="img"><title>Generic cloud services symbol for gcp; not an official logo</title><rect x="3" y="3" width="18" height="18" rx="3"/><rect x="6" y="7" width="4" height="4"/><rect x="14" y="7" width="4" height="4"/><path d="M8 15h8M12 11v7"/></svg>
```

Source: Newly authored basic SVG geometry for Blitz v2.1OAI, 11-10-2026. See `../THIRD_PARTY_LICENSES.md` for provenance and the complete replacement inventory.

### postgres
PostgreSQL. Uses a generic database symbol, not an official product logo. Keep the product name as a separate text label.

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" role="img"><title>Generic database symbol for postgres; not an official logo</title><ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v13c0 4 16 4 16 0V5M4 11c0 4 16 4 16 0M4 17c0 4 16 4 16 0"/></svg>
```

Source: Newly authored basic SVG geometry for Blitz v2.1OAI, 11-10-2026. See `../THIRD_PARTY_LICENSES.md` for provenance and the complete replacement inventory.

### redis
Redis. Uses a generic memory cache symbol, not an official product logo. Keep the product name as a separate text label.

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" role="img"><title>Generic memory cache symbol for redis; not an official logo</title><rect x="3" y="4" width="18" height="6" rx="1"/><rect x="3" y="14" width="18" height="6" rx="1"/><path d="M7 7h4M7 17h4M16 7h1M16 17h1M12 10v4"/></svg>
```

Source: Newly authored basic SVG geometry for Blitz v2.1OAI, 11-10-2026. See `../THIRD_PARTY_LICENSES.md` for provenance and the complete replacement inventory.

### nginx
Nginx. Uses a generic web gateway symbol, not an official product logo. Keep the product name as a separate text label.

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" role="img"><title>Generic web gateway symbol for nginx; not an official logo</title><rect x="8" y="3" width="8" height="18" rx="1"/><path d="M2 8h10l-2-2M12 8l-2 2M22 16H12l2-2M12 16l2 2"/></svg>
```

Source: Newly authored basic SVG geometry for Blitz v2.1OAI, 11-10-2026. See `../THIRD_PARTY_LICENSES.md` for provenance and the complete replacement inventory.

### gitea
Gitea self-hosted Git. Uses a generic source repository symbol, not an official product logo. Keep the product name as a separate text label.

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" role="img"><title>Generic source repository symbol for gitea; not an official logo</title><rect x="3" y="3" width="18" height="18" rx="1"/><circle cx="8" cy="7" r="1.5"/><circle cx="8" cy="17" r="1.5"/><circle cx="16" cy="9" r="1.5"/><path d="M8 8.5v7M8 12h8v-1.5"/></svg>
```

Source: Newly authored basic SVG geometry for Blitz v2.1OAI, 11-10-2026. See `../THIRD_PARTY_LICENSES.md` for provenance and the complete replacement inventory.

### keycloak
Keycloak identity / SSO. Uses a generic identity service symbol, not an official product logo. Keep the product name as a separate text label.

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" role="img"><title>Generic identity service symbol for keycloak; not an official logo</title><rect x="3" y="3" width="18" height="18" rx="1"/><circle cx="8" cy="9" r="2"/><path d="M5 16v-1c0-3 6-3 6 0v1M15 8h3M15 12h3M15 16h3"/></svg>
```

Source: Newly authored basic SVG geometry for Blitz v2.1OAI, 11-10-2026. See `../THIRD_PARTY_LICENSES.md` for provenance and the complete replacement inventory.

### active-directory
Active Directory / LDAP identity directory.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6v12a2 2 0 0 1 -2 2h-10a2 2 0 0 1 -2 -2v-12a2 2 0 0 1 2 -2h10a2 2 0 0 1 2 2" /> <path d="M10 16h6" /> <path d="M11 11a2 2 0 1 0 4 0a2 2 0 1 0 -4 0" /> <path d="M4 8h3" /> <path d="M4 12h3" /> <path d="M4 16h3" /></svg>
```

Source: Tabler Icons / `address-book` (MIT)

### minio
MinIO S3-compatible object storage. Uses a generic object storage symbol, not an official product logo. Keep the product name as a separate text label.

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" role="img"><title>Generic object storage symbol for minio; not an official logo</title><rect x="3" y="4" width="18" height="16" rx="1"/><path d="M3 9h18M9 9v11M15 9v11M3 14h18M8 6.5h8"/></svg>
```

Source: Newly authored basic SVG geometry for Blitz v2.1OAI, 11-10-2026. See `../THIRD_PARTY_LICENSES.md` for provenance and the complete replacement inventory.

### mysql
MySQL. Uses a generic database symbol, not an official product logo. Keep the product name as a separate text label.

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" role="img"><title>Generic database symbol for mysql; not an official logo</title><ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v13c0 4 16 4 16 0V5M4 11c0 4 16 4 16 0M4 17c0 4 16 4 16 0"/></svg>
```

Source: Newly authored basic SVG geometry for Blitz v2.1OAI, 11-10-2026. See `../THIRD_PARTY_LICENSES.md` for provenance and the complete replacement inventory.

### oracle
Oracle Database. Uses a generic database symbol, not an official product logo. Keep the product name as a separate text label.

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" role="img"><title>Generic database symbol for oracle; not an official logo</title><ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v13c0 4 16 4 16 0V5M4 11c0 4 16 4 16 0M4 17c0 4 16 4 16 0"/></svg>
```

Source: Newly authored basic SVG geometry for Blitz v2.1OAI, 11-10-2026. See `../THIRD_PARTY_LICENSES.md` for provenance and the complete replacement inventory.

### sqlserver
Microsoft SQL Server. Uses a generic database symbol, not an official product logo. Keep the product name as a separate text label.

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" role="img"><title>Generic database symbol for sqlserver; not an official logo</title><ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v13c0 4 16 4 16 0V5M4 11c0 4 16 4 16 0M4 17c0 4 16 4 16 0"/></svg>
```

Source: Newly authored basic SVG geometry for Blitz v2.1OAI, 11-10-2026. See `../THIRD_PARTY_LICENSES.md` for provenance and the complete replacement inventory.

### sqlite
SQLite embedded database. Uses a generic database symbol, not an official product logo. Keep the product name as a separate text label.

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" role="img"><title>Generic database symbol for sqlite; not an official logo</title><ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v13c0 4 16 4 16 0V5M4 11c0 4 16 4 16 0M4 17c0 4 16 4 16 0"/></svg>
```

Source: Newly authored basic SVG geometry for Blitz v2.1OAI, 11-10-2026. See `../THIRD_PARTY_LICENSES.md` for provenance and the complete replacement inventory.

### hive
Apache Hive data warehouse. Uses a generic database symbol, not an official product logo. Keep the product name as a separate text label.

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" role="img"><title>Generic database symbol for hive; not an official logo</title><ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v13c0 4 16 4 16 0V5M4 11c0 4 16 4 16 0M4 17c0 4 16 4 16 0"/></svg>
```

Source: Newly authored basic SVG geometry for Blitz v2.1OAI, 11-10-2026. See `../THIRD_PARTY_LICENSES.md` for provenance and the complete replacement inventory.

### starrocks
StarRocks MPP analytical database. Uses a generic database symbol, not an official product logo. Keep the product name as a separate text label.

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" role="img"><title>Generic database symbol for starrocks; not an official logo</title><ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v13c0 4 16 4 16 0V5M4 11c0 4 16 4 16 0M4 17c0 4 16 4 16 0"/></svg>
```

Source: Newly authored basic SVG geometry for Blitz v2.1OAI, 11-10-2026. See `../THIRD_PARTY_LICENSES.md` for provenance and the complete replacement inventory.

## Data stack

### nifi
Apache NiFi data flow. Uses a generic data pipeline symbol, not an official product logo. Keep the product name as a separate text label.

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" role="img"><title>Generic data pipeline symbol for nifi; not an official logo</title><rect x="2" y="9" width="5" height="6" rx="1"/><rect x="9.5" y="9" width="5" height="6" rx="1"/><rect x="17" y="9" width="5" height="6" rx="1"/><path d="M7 12h2.5M14.5 12H17M12 9V5h7v4"/></svg>
```

Source: Newly authored basic SVG geometry for Blitz v2.1OAI, 11-10-2026. See `../THIRD_PARTY_LICENSES.md` for provenance and the complete replacement inventory.

### airflow
Apache Airflow scheduler / DAG runner. Uses a generic task dependencies symbol, not an official product logo. Keep the product name as a separate text label.

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" role="img"><title>Generic task dependencies symbol for airflow; not an official logo</title><rect x="2" y="9.5" width="5" height="5" rx="1"/><rect x="10" y="2" width="5" height="5" rx="1"/><rect x="10" y="17" width="5" height="5" rx="1"/><rect x="18" y="9.5" width="4" height="5" rx="1"/><path d="M7 12h1.5V4.5H10M8.5 12v7.5H10M15 4.5h1.5V12H18M15 19.5h1.5V12"/></svg>
```

Source: Newly authored basic SVG geometry for Blitz v2.1OAI, 11-10-2026. See `../THIRD_PARTY_LICENSES.md` for provenance and the complete replacement inventory.

### hop
Apache Hop data orchestration / ETL. Uses a generic data pipeline symbol, not an official product logo. Keep the product name as a separate text label.

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" role="img"><title>Generic data pipeline symbol for hop; not an official logo</title><rect x="2" y="9" width="5" height="6" rx="1"/><rect x="9.5" y="9" width="5" height="6" rx="1"/><rect x="17" y="9" width="5" height="6" rx="1"/><path d="M7 12h2.5M14.5 12H17M12 9V5h7v4"/></svg>
```

Source: Newly authored basic SVG geometry for Blitz v2.1OAI, 11-10-2026. See `../THIRD_PARTY_LICENSES.md` for provenance and the complete replacement inventory.

### pentaho
Pentaho PDI (Kettle) ETL and data integration. Uses a generic data merge symbol, not an official product logo. Keep the product name as a separate text label.

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" role="img"><title>Generic data merge symbol for pentaho; not an official logo</title><rect x="2" y="3" width="6" height="5" rx="1"/><rect x="2" y="16" width="6" height="5" rx="1"/><rect x="16" y="9.5" width="6" height="5" rx="1"/><path d="M8 5.5h3V12h5M8 18.5h3V12M13.5 10l2.5 2-2.5 2"/></svg>
```

Source: Newly authored basic SVG geometry for Blitz v2.1OAI, 11-10-2026. See `../THIRD_PARTY_LICENSES.md` for provenance and the complete replacement inventory.

### dagster
Dagster data orchestration platform. Uses a generic task dependencies symbol, not an official product logo. Keep the product name as a separate text label.

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" role="img"><title>Generic task dependencies symbol for dagster; not an official logo</title><rect x="2" y="9.5" width="5" height="5" rx="1"/><rect x="10" y="2" width="5" height="5" rx="1"/><rect x="10" y="17" width="5" height="5" rx="1"/><rect x="18" y="9.5" width="4" height="5" rx="1"/><path d="M7 12h1.5V4.5H10M8.5 12v7.5H10M15 4.5h1.5V12H18M15 19.5h1.5V12"/></svg>
```

Source: Newly authored basic SVG geometry for Blitz v2.1OAI, 11-10-2026. See `../THIRD_PARTY_LICENSES.md` for provenance and the complete replacement inventory.

### trino
Trino distributed SQL query engine. Uses a generic database symbol, not an official product logo. Keep the product name as a separate text label.

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" role="img"><title>Generic database symbol for trino; not an official logo</title><ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v13c0 4 16 4 16 0V5M4 11c0 4 16 4 16 0M4 17c0 4 16 4 16 0"/></svg>
```

Source: Newly authored basic SVG geometry for Blitz v2.1OAI, 11-10-2026. See `../THIRD_PARTY_LICENSES.md` for provenance and the complete replacement inventory.

### superset
Apache Superset BI / dashboards. Uses a generic analytics dashboard symbol, not an official product logo. Keep the product name as a separate text label.

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" role="img"><title>Generic analytics dashboard symbol for superset; not an official logo</title><rect x="2" y="3" width="20" height="18" rx="1"/><path d="M2 7h20M6 17v-5M11 17v-7M16 17v-3M5 17h13"/></svg>
```

Source: Newly authored basic SVG geometry for Blitz v2.1OAI, 11-10-2026. See `../THIRD_PARTY_LICENSES.md` for provenance and the complete replacement inventory.

### redash
Redash BI / dashboards. Uses a generic analytics dashboard symbol, not an official product logo. Keep the product name as a separate text label.

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" role="img"><title>Generic analytics dashboard symbol for redash; not an official logo</title><rect x="2" y="3" width="20" height="18" rx="1"/><path d="M2 7h20M6 17v-5M11 17v-7M16 17v-3M5 17h13"/></svg>
```

Source: Newly authored basic SVG geometry for Blitz v2.1OAI, 11-10-2026. See `../THIRD_PARTY_LICENSES.md` for provenance and the complete replacement inventory.

### tableau
Tableau data visualization. Uses a generic analytics dashboard symbol, not an official product logo. Keep the product name as a separate text label.

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" role="img"><title>Generic analytics dashboard symbol for tableau; not an official logo</title><rect x="2" y="3" width="20" height="18" rx="1"/><path d="M2 7h20M6 17v-5M11 17v-7M16 17v-3M5 17h13"/></svg>
```

Source: Newly authored basic SVG geometry for Blitz v2.1OAI, 11-10-2026. See `../THIRD_PARTY_LICENSES.md` for provenance and the complete replacement inventory.

### powerbi
Microsoft Power BI. Uses a generic analytics dashboard symbol, not an official product logo. Keep the product name as a separate text label.

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" role="img"><title>Generic analytics dashboard symbol for powerbi; not an official logo</title><rect x="2" y="3" width="20" height="18" rx="1"/><path d="M2 7h20M6 17v-5M11 17v-7M16 17v-3M5 17h13"/></svg>
```

Source: Newly authored basic SVG geometry for Blitz v2.1OAI, 11-10-2026. See `../THIRD_PARTY_LICENSES.md` for provenance and the complete replacement inventory.

### jupyter
Jupyter / JupyterLab notebooks. Uses a generic code notebook symbol, not an official product logo. Keep the product name as a separate text label.

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" role="img"><title>Generic code notebook symbol for jupyter; not an official logo</title><rect x="5" y="2" width="16" height="20" rx="1"/><path d="M3 6h4M3 11h4M3 16h4M3 21h4M11 8l-2 2 2 2M15 8l2 2-2 2M10 17h7"/></svg>
```

Source: Newly authored basic SVG geometry for Blitz v2.1OAI, 11-10-2026. See `../THIRD_PARTY_LICENSES.md` for provenance and the complete replacement inventory.

## Language

### python
Python programming language. Uses a generic code runtime symbol, not an official product logo. Keep the product name as a separate text label.

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" role="img"><title>Generic code runtime symbol for python; not an official logo</title><rect x="2" y="4" width="20" height="16" rx="1"/><path d="M8 8l-3 4 3 4M16 8l3 4-3 4M13.5 8l-3 8"/></svg>
```

Source: Newly authored basic SVG geometry for Blitz v2.1OAI, 11-10-2026. See `../THIRD_PARTY_LICENSES.md` for provenance and the complete replacement inventory.

### r
R statistical language. Uses a generic statistical analysis symbol, not an official product logo. Keep the product name as a separate text label.

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" role="img"><title>Generic statistical analysis symbol for r; not an official logo</title><rect x="3" y="3" width="18" height="18" rx="1"/><path d="M7 17V9M12 17V6M17 17v-5M6 17h12M5 7h4"/></svg>
```

Source: Newly authored basic SVG geometry for Blitz v2.1OAI, 11-10-2026. See `../THIRD_PARTY_LICENSES.md` for provenance and the complete replacement inventory.

### sql
SQL / generic relational query.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 8a2 2 0 0 1 2 2v4a2 2 0 1 1 -4 0v-4a2 2 0 0 1 2 -2" /> <path d="M17 8v8h4" /> <path d="M13 15l1 1" /> <path d="M3 15a1 1 0 0 0 1 1h2a1 1 0 0 0 1 -1v-2a1 1 0 0 0 -1 -1h-2a1 1 0 0 1 -1 -1v-2a1 1 0 0 1 1 -1h2a1 1 0 0 1 1 1" /></svg>
```

Source: Tabler Icons / `sql` (MIT)

## Statistical tools

### spss
IBM SPSS Statistics. Uses a generic statistical analysis symbol, not an official product logo. Keep the product name as a separate text label.

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" role="img"><title>Generic statistical analysis symbol for spss; not an official logo</title><rect x="3" y="3" width="18" height="18" rx="1"/><path d="M7 17V9M12 17V6M17 17v-5M6 17h12M5 7h4"/></svg>
```

Source: Newly authored basic SVG geometry for Blitz v2.1OAI, 11-10-2026. See `../THIRD_PARTY_LICENSES.md` for provenance and the complete replacement inventory.

### sas
SAS statistical analysis. Uses a generic statistical analysis symbol, not an official product logo. Keep the product name as a separate text label.

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" role="img"><title>Generic statistical analysis symbol for sas; not an official logo</title><rect x="3" y="3" width="18" height="18" rx="1"/><path d="M7 17V9M12 17V6M17 17v-5M6 17h12M5 7h4"/></svg>
```

Source: Newly authored basic SVG geometry for Blitz v2.1OAI, 11-10-2026. See `../THIRD_PARTY_LICENSES.md` for provenance and the complete replacement inventory.

### stata
Stata statistical analysis. Uses a generic statistical analysis symbol, not an official product logo. Keep the product name as a separate text label.

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" role="img"><title>Generic statistical analysis symbol for stata; not an official logo</title><rect x="3" y="3" width="18" height="18" rx="1"/><path d="M7 17V9M12 17V6M17 17v-5M6 17h12M5 7h4"/></svg>
```

Source: Newly authored basic SVG geometry for Blitz v2.1OAI, 11-10-2026. See `../THIRD_PARTY_LICENSES.md` for provenance and the complete replacement inventory.

### rstudio
RStudio / Posit IDE for R and Python. Uses a generic code workspace symbol, not an official product logo. Keep the product name as a separate text label.

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" role="img"><title>Generic code workspace symbol for rstudio; not an official logo</title><rect x="2" y="3" width="20" height="18" rx="1"/><path d="M2 8h20M8 8v13M5 5.5h1M11 12l-2 2 2 2M17 12l2 2-2 2M14.5 11l-2 6"/></svg>
```

Source: Newly authored basic SVG geometry for Blitz v2.1OAI, 11-10-2026. See `../THIRD_PARTY_LICENSES.md` for provenance and the complete replacement inventory.

### qgis
QGIS geographic information system. Uses a generic geographic data symbol, not an official product logo. Keep the product name as a separate text label.

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" role="img"><title>Generic geographic data symbol for qgis; not an official logo</title><rect x="3" y="3" width="18" height="18" rx="1"/><path d="M9 3v18M15 3v18M3 9h18M3 15h18"/><circle cx="12" cy="12" r="2"/></svg>
```

Source: Newly authored basic SVG geometry for Blitz v2.1OAI, 11-10-2026. See `../THIRD_PARTY_LICENSES.md` for provenance and the complete replacement inventory.

## File formats

### excel
Microsoft Excel spreadsheet.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14 3v4a1 1 0 0 0 1 1h4" /> <path d="M5 12v-7a2 2 0 0 1 2 -2h7l5 5v4" /> <path d="M4 15l4 6" /> <path d="M4 21l4 -6" /> <path d="M17 20.25c0 .414 .336 .75 .75 .75h1.25a1 1 0 0 0 1 -1v-1a1 1 0 0 0 -1 -1h-1a1 1 0 0 1 -1 -1v-1a1 1 0 0 1 1 -1h1.25a.75 .75 0 0 1 .75 .75" /> <path d="M11 15v6h3" /></svg>
```

Source: Tabler Icons / `file-type-xls` (MIT)

### csv
Comma-separated values file.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14 3v4a1 1 0 0 0 1 1h4" /> <path d="M5 12v-7a2 2 0 0 1 2 -2h7l5 5v4" /> <path d="M7 16.5a1.5 1.5 0 0 0 -3 0v3a1.5 1.5 0 0 0 3 0" /> <path d="M10 20.25c0 .414 .336 .75 .75 .75h1.25a1 1 0 0 0 1 -1v-1a1 1 0 0 0 -1 -1h-1a1 1 0 0 1 -1 -1v-1a1 1 0 0 1 1 -1h1.25a.75 .75 0 0 1 .75 .75" /> <path d="M16 15l2 6l2 -6" /></svg>
```

Source: Tabler Icons / `file-type-csv` (MIT)

### txt
Plain text file.

```svg
<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14 3v4a1 1 0 0 0 1 1h4" /> <path d="M14 3v4a1 1 0 0 0 1 1h4" /> <path d="M16.5 15h3" /> <path d="M5 12v-7a2 2 0 0 1 2 -2h7l5 5v4" /> <path d="M4.5 15h3" /> <path d="M6 15v6" /> <path d="M18 15v6" /> <path d="M10 15l4 6" /> <path d="M10 21l4 -6" /></svg>
```

Source: Tabler Icons / `file-type-txt` (MIT)

---

## License attribution

- **Tabler Icons**, MIT, https://github.com/tabler/tabler-icons. Only generic symbols remain from this collection; no `brand-*` glyphs are included.
- **Blitz generic stand-ins**, newly authored SVG geometry for 37 product keys. Product names serve as text labels, not as claims that these symbols are official logos.

See `../THIRD_PARTY_LICENSES.md` for the retained MIT notice, replacement inventory, provenance limits, and trademark guidance. Icon-source notices do not establish a blanket license for the Blitz repository.
