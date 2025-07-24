import {
  mdiMenu,
  mdiClockOutline,
  mdiCloud,
  mdiCrop,
  mdiLogout,
  mdiThemeLightDark,
  mdiGithub,
  mdiReact,
  mdiBox,
  mdiAccountGroup,
  mdiCartOutline,
  mdiChartLine,
  mdiRefresh,
} from '@mdi/js'

export default [
  {
    icon: mdiMenu,
    label: 'Sample menu',
    menu: [
      {
        icon: mdiClockOutline,
        label: 'Item One',
      },
      {
        icon: mdiCloud,
        label: 'Item Two',
      },
      {
        isDivider: true,
      },
      {
        icon: mdiCrop,
        label: 'Item Last',
      },
    ],
  },
  {
    isCurrentUser: true,
    menu: [
      {
        label: 'My Profile',
        to: '/profile',
      },
      {
        label: 'Settings',
        to: '/parametre',
      },
      {
        label: 'Messages',
      },
      {
        isDivider: true,
      },
      {
        label: 'Log Out',
        isLogout: true,
      },
    ],
  },
  {
    icon: mdiThemeLightDark,
    label: 'Light/Dark',
    isDesktopNoLabel: true,
    isToggleLightDark: true,
  },
  {
    icon: mdiGithub,
    label: 'GitHub',
    isDesktopNoLabel: true,
    href: 'https://github.com/justboil/admin-one-vue-tailwind',
    target: '_blank',
  },
  {
    icon: mdiReact,
    label: 'React version',
    isDesktopNoLabel: true,
    href: 'https://github.com/justboil/admin-one-react-tailwind',
    target: '_blank',
  },
  {
    icon: mdiBox,
    label: 'Produits',
    to: '/produits',
  },
  {
    icon: mdiAccountGroup,
    label: 'Fournisseurs',
    to: '/fournisseurs',
  },
  {
    icon: mdiCartOutline,
    label: 'Commandes Fournisseurs',
    to: '/commandes-fournisseurs',
  },
  {
    icon: mdiChartLine,
    label: 'Historique Ventes',
    to: '/historique-ventes',
  },
  {
    icon: mdiRefresh,
    label: 'Approvisionnements Auto',
    to: '/approvisionnements-auto',
  },
  {
    icon: mdiLogout,
    label: 'Log out',
    isDesktopNoLabel: true,
    isLogout: true,
  },
]
